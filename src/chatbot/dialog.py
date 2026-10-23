from google import genai
from google.genai import types
from google.genai import types
from google.genai import errors
from src.chatbot.dialog_information import general_information, information_zone, information_character
from src.escape_room.application.context_manager import ContextManager

class Dialog():
    def __init__(self):
        self.client = ContextManager().get_chatbot_client()
        self.first_message = True
        self.chat_id = None
        self.messages = []

    def talk_with_npc(self, player_role, figure, player_message, speech, speech_bubble):
        chatbot_type = self.client.get_chatbot_type()
        if chatbot_type=='LLM':
            zone_id = speech.model_mapping[speech['name']]['information_zone']
            npc = speech.model_mapping[speech['name']]['non_player_character']
            if self.first_message:
                message = general_information + information_zone[zone_id] + information_character[npc]
                message += player_role + " says: " + player_message
            else:
                message = player_role + " says: " + player_message
        elif chatbot_type=='SLM':
            message = "User (" + player_role + "): " + player_message
        output_text = self.client.send_message(message,self.first_message,player_role,figure,speech,speech_bubble,self)
        return output_text

    def reset_dialog(self):
        self.first_message = True
        self.client.reset()
        self.messages = []

    def add_message(self,message,figure_name):
        self.messages.append((message,figure_name))

    def get_message_history(self):
        text = ""
        for (message,_) in self.messages:
            text += message + '\n'
        return text
