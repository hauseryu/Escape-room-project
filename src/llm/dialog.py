from google import genai
from google.genai import types
from google.genai import types
from google.genai import errors
from src.llm.dialog_information import general_information, information_zone, information_character
from src.escape_room.application.context_manager import ContextManager

class Dialog():
    def __init__(self):
        self.client = ContextManager().get_llm_client().client
        self.first_message = True
        self.chat_id = None

    def talk_with_npc(self, npc, player, player_message):
        if self.first_message:
            if npc <= 2:
                zone_id = 0
                player1 = "Sherlock Holmes"
                player2 = "Dr. John Watson"
            elif npc <= 4:
                zone_id = 1
                player1 = "Harry Potter"
                player2 = "Hermione Granger"
            else:
                zone_id = 2
                player1 = "Player 1"
                player2 = "Player 2"
            message = general_information + information_zone[zone_id] + information_character[npc]
            if player == 0:
                message += player1 + " says: " + player_message
            elif player == 1:
                message += player2 + " says: " + player_message
            try:
                    interaction = self.client.interactions.create(
                    model="gemini-3.8-flash",
                    input=message
                )
            except errors.APIError as e:
                print("Gemini API Fehler:")
                print("Code:", e.code)
                print("Nachricht:", e.message)
                raise
        else:
            if player == 0:
                message = player1 + " says: " + player_message
            elif player == 1:
                message = player2 + " says: " + player_message
            interaction = self.client.interactions.create(
                model="gemini-3.8-flash",
                input=message,
                previous_interaction_id=self.chat_id
            )

        self.chat_id = interaction.id
        return interaction.output_text

    def reset_dialog(self):
        self.first_message = True
        self.chat_id = None
