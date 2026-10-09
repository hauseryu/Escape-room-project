from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path
import threading
import ollama
from google.genai import types
from google.genai import errors
from src.escape_room.application.context_manager import ContextManager

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

    def send_message(self,message,first_message):
        if CHATBOT_TYPE=='LLM':
            return self.send_message_llm(message,first_message)

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

    def reset(self):
        self.chat_id = None

    def send_message_simple(self,system_prompt,user_prompt,speech_bubble=None,chatbot_callback=None):
        if CHATBOT_TYPE=='LLM':
            return self.send_message_simple_llm(system_prompt+user_prompt)
        elif CHATBOT_TYPE=='SLM':
            return self.send_message_simple_slm(system_prompt,user_prompt,speech_bubble,chatbot_callback)
        
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

    def send_message_simple_slm(self,system_prompt,user_prompt,speech_bubble,chatbot_callback):
        stream_thread = threading.Thread(target=self._stream_prozess, args=(system_prompt,user_prompt,speech_bubble, chatbot_callback))
        stream_thread.daemon = True
        stream_thread.start()

    def _stream_prozess(self, system_prompt,user_prompt, speech_bubble, chatbot_callback):
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
                
                # each fragment is passed to GUI via .after() 
                canvas.after(0, self._add_word_fragment, word_fragment,speech_bubble)
                
        except Exception as e:
            canvas.after(0, self._add_word_fragment, f"\n[Fehler: {e}]",speech_bubble)
            
        # finally, return the whole text to the chatbot callcack function
        canvas.after(0, lambda: chatbot_callback(text))

    def _add_word_fragment(self, text, speech_bubble):
        # write word fragment to end of text field and scroll automatically
        if speech_bubble!=None:
            speech_bubble.add_word_to_text_area(text)
      