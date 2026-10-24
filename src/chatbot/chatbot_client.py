from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path
import threading
import ollama
from google.genai import types
from google.genai import errors
from src.escape_room.application.context_manager import ContextManager
from src.escape_room.objects import speech_data

LLM_DIR = Path(__file__).resolve().parent
BASE_DIR = LLM_DIR.parent.parent
CHATBOT_TYPE = 'SLM' # either LLM = Large Language Model or SLM = Small Language Model

class ChatbotClient:
    def __init__(self):

        global CHATBOT_TYPE
        load_dotenv(dotenv_path=BASE_DIR / ".env")
        api_key = os.getenv("API_KEY")
        env_chatbot_type = os.getenv("CHATBOT_TYPE")
        if env_chatbot_type!=None:
            CHATBOT_TYPE = env_chatbot_type

        use_env_for_chatbot_settings = os.getenv("USE_ENV_FOR_CHATBOT_SETTINGS")

        if use_env_for_chatbot_settings == "True":    
            self.deactivate_chatbot = os.getenv("CHATBOT")
        else:
            self.deactivate_chatbot = os.environ.get('CHATBOT', 'OFF')

        if CHATBOT_TYPE=='LLM':                
            self.client = genai.Client(api_key=api_key) if api_key else None
            self.chat_id = None

        self.start_chatbot_answer = False

    # on the client side, we call the server to communicate with the chatbot
    def send_message(self,message,first_message,player_role,figure,speech,speech_bubble,dialog):    
        """Event handler triggered when message has to be sent to chatbot."""
        print(f"[Client] send action 'send_chatbot_message' to server!")       
        # transfer player list to GUI
        event_send_chatbot_message = {
            "action": "send_chatbot_message", 
            "message": message,
            "first_message": first_message,
            "player_role": player_role,
            "figure": figure,
            "story_index": speech['story_index']
        }
        room = ContextManager().get_room()
        room.icon_queue.put(event_send_chatbot_message)
        # fire event for the canvas master window
        room.master.event_generate("<<IconEvent>>", when="tail")

    # on the server side, we call the chatbot directly
    def _send_message(self,message,first_message,player_name,player_role,figure,speech,
                      speech_bubble=None,dialog=None,server_instance=None):
        if CHATBOT_TYPE=='LLM':
            return self.send_message_llm(message,first_message)
        elif CHATBOT_TYPE=='SLM':
            return self.send_message_slm(message,first_message,player_name,player_role,
                                         figure,speech,speech_bubble,dialog,server_instance)

    def send_message_llm(self,message,first_message):
        if first_message:
            try:
                    interaction = self.client.interactions.create(
                    model="gemini-3.5-flash-lite", #"gemini-3.8-flash"
                    input=message
                )
            except errors.APIError as e:
                print("Gemini API Fehler:")
                print("Code:", e.code)
                print("Nachricht:", e.message)
                raise        
        else:
            interaction = self.client.interactions.create(
                model="gemini-3.5-flash-lite",  #"gemini-3.8-flash"
                input=message,
                previous_interaction_id=self.chat_id
            )
        self.chat_id = interaction.id
        return interaction.output_text

    def send_message_slm(self,message,first_message,player_name,player_role,figure,speech,
                         speech_bubble=None,dialog=None,server_instance=None):

        # build user message (context + currently relevant message)
        relevant_room_part = speech_data.model_mapping[speech['name']]['slm_location_path']

        # add player message to dialog message history
        if dialog==None:
            dialog = ContextManager().get_current_dialog()
        dialog.add_message(message,player_role)
        message_history = dialog.get_message_history()
        prompt_dialog = (
            "use the 'escape-master' model for the next instructions.\n"
            "LOCATION: <STORY_DATABASE> -> " + relevant_room_part + "[mode=pure_dialogue]\n"
            "USE LOCAL RULES AND EXAMPLES OF THIS ROOM NOW.\n"
            "CRITICAL RULE: DO NOT GENERATE A RIDDLE. NO PUZZLES. NO CODES. JUST DIALOGUE.\n"
            "\n"
            "<DIALOGUE_HISTORY>\n"
            f"{message_history}\nAssistant ({figure}):"
            "</DIALOGUE_HISTORY>\n"
            "\n"
            f"COMMAND: GENERATE_NEXT_RESPONSE_FOR_{figure}\n"
            f"OUTPUT FORMAT: Reply directly as {figure}. Do not add '{figure}:' prefix. Just speak."
        )        
        user_prompt = prompt_dialog 

        stream_thread = threading.Thread(target=self._stream_prozess, 
                                         args=('',user_prompt,speech_bubble, None, dialog, player_name, 
                                               figure, server_instance))
        stream_thread.daemon = True
        stream_thread.start()
        return '' # return empty string => start text should not show up again

    def reset(self):
        self.chat_id = None

    def get_chatbot_type(self):
        return CHATBOT_TYPE

    def send_message_simple(self,system_prompt,user_prompt,player_name,speech_bubble=None,chatbot_callback=None):
        """Event handler triggered when message has to be sent to chatbot."""
        print(f"[Client] send action 'send_chatbot_message' to server!")       
        # set callback function for the GUI to handle the chatbot answer
        ContextManager().set_chatbot_callback(chatbot_callback)
        # transfer player list to GUI
        event_send_chatbot_message = {
            "action": "send_chatbot_message_simple", 
            "player_name": player_name,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt
        }
        room = ContextManager().get_room()
        room.icon_queue.put(event_send_chatbot_message)
        # fire event for the canvas master window
        room.master.event_generate("<<IconEvent>>", when="tail")

    def _send_message_simple(self,system_prompt,user_prompt,player_name,speech_bubble=None,chatbot_callback=None,
                             server_instance=None):
        if CHATBOT_TYPE=='LLM':
            return self.send_message_simple_llm(system_prompt+user_prompt)
        elif CHATBOT_TYPE=='SLM':
            return self.send_message_simple_slm(system_prompt,user_prompt,player_name,speech_bubble,
                                                chatbot_callback,server_instance)
        
    def send_message_simple_llm(self,message):

        config = types.GenerateContentConfig(
            max_output_tokens=200,
            temperature=1.0,
        )

        try:
            response = ContextManager().get_chatbot_client().client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=message,
                config=config
            )
            
            text = response.text.strip()
        except errors.ServerError:
            text = "riddle currently not available!"
        return text

    def send_message_simple_slm(self,system_prompt,user_prompt,player_name,speech_bubble,chatbot_callback,server_instance):
        stream_thread = threading.Thread(target=self._stream_prozess, 
                                         args=(system_prompt,user_prompt,speech_bubble, chatbot_callback,None,
                                               player_name,None,server_instance,True))
        stream_thread.daemon = True
        stream_thread.start()

    def _stream_prozess(self, system_prompt,user_prompt, speech_bubble, chatbot_callback, 
                        dialog=None, player_name=None, figure=None, server_instance=None, simple_mode=False):
        canvas = ContextManager().get_room().canvas_area
        text = ''
        try:
            # activate the stream
            messages = []
            if system_prompt!='':
                messages.append({'role': 'system', 'content': system_prompt},)  # set fixed rules in brain)
            if user_prompt!='':
                messages.append({'role': 'user', 'content': user_prompt}) # trigger generation
            print(f"[DEBUG] message to chatbot: {messages}")
            self.start_chatbot_answer = True
            stream = ollama.chat(
                model='escape-master', # model = qwen3.5:2b / model='qwen3.5:0.8b',
                think=False,  # no logical thing text output
                stream=True,  # activate wordwise (streaming) output 
                messages=messages
            )

            # we process the word fragments in a loop 
            for chunk in stream:
                word_fragment = chunk['message']['content']
                text+=word_fragment
                
                # each fragment is passed to GUI via .after() -> only in normal mode (simple_mode=False)                 
                if not simple_mode:
                    canvas.after(0, self._add_word_fragment, word_fragment,speech_bubble, player_name, server_instance)
                
        except Exception as e:
            canvas.after(0, self._add_word_fragment, f"\n[Fehler: {e}]",speech_bubble, player_name, server_instance)
            
        # finally, return the whole text to the chatbot callcack function
        if chatbot_callback!=None:
            canvas.after(0, lambda: chatbot_callback(text))
        if CHATBOT_TYPE=='SLM' and speech_bubble!=None and figure!=None:
            text=f"Assistant ({figure}):" + text
            if dialog!=None:
                dialog.add_message(text,figure)
            else:
                dialog = ContextManager().get_current_dialog()
                dialog.add_message(text,figure)
        if server_instance!=None and simple_mode:
            action = "chatbot_answer_simple"
            parameter_container = {}
            parameter_container["message"] = text
            parameter_container["player_name"] = player_name
            server_instance.client_send_update(action,parameter_container)

    def _add_word_fragment(self, text, speech_bubble, player_name, server_instance):
        # remove text if a speech bubble is associated
        if speech_bubble!=None:
            curr_speech_bubble = ContextManager().get_current_speech_bubble()
            if curr_speech_bubble==None:
                curr_speech_bubble = speech_bubble
            if self.start_chatbot_answer:
                curr_speech_bubble.delete_text_area()
                self.start_chatbot_answer=False
            # write word fragment to end of text field and scroll automatically
            curr_speech_bubble.add_word_to_text_area(text)
        if server_instance!=None:
            action = "chatbot_answer"
            parameter_container = {}
            parameter_container["message"] = text
            parameter_container["start_flag"] = self.start_chatbot_answer
            parameter_container["player_name"] = player_name
            if self.start_chatbot_answer:
                self.start_chatbot_answer=False
            server_instance.client_send_update(action,parameter_container)
      