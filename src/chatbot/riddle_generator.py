from calendar import c
from urllib import response

from google import genai
from google.genai import types
from google.genai import errors
import os
from dotenv import load_dotenv
import random
from pathlib import Path
from src.escape_room.application.context_manager import ContextManager

RIDDLES_DIR = Path(__file__).resolve().parent
THEMES_FILE = RIDDLES_DIR / "themes.txt"

with open(THEMES_FILE, "r", encoding="utf-8") as file:
    THEMES = [line.strip() for line in file if line.strip()]

def generate_riddle(chatbot_callback=None):

    selected_themes = random.sample(THEMES, 3)
    themes_text = ", ".join(selected_themes)
    
    if ContextManager().get_chatbot_client().deactivate_chatbot == 'OFF':
        print("[DEBUG] riddle is currently deactivated by system/env variable CHATBOT=OFF")
        return ("riddle not available","1")

    # rules and format are sent via the system role
    # system_prompt = f"""
    # You are a precise riddle generator for an escape room. 
    # Your only task is to create a short riddle based strictly on the user's topics and output it EXACTLY in the required format.

    # RULES:
    # - Use 2 to 3 of the given topics.
    # - Maximum 2-3 short sentences for the riddle.
    # - You MUST generate exactly FOUR options (labeled 1, 2, 3, 4). 
    # - Exactly one option must be the mathematically/logically correct answer.
    # - Do not use * or ** anywhere.
    # - Never skip the options. Never shorten the output.

    # OUTPUT TEMPLATE (You must follow this text structure identically):

    # Riddle:
    # [Write the riddle here]

    # 1) [Option 1]
    # 2) [Option 2]
    # 3) [Option 3]
    # 4) [Option 4]

    # Correct answer (only the number):
    # [Only the number 1, 2, 3, or 4]

    # EXAMPLE OF PERFECTION:
    # Riddle:
    # I am a box without hinges, key, or lid, yet golden treasure inside me is hid. What am I?

    # 1) A chest
    # 2) An egg
    # 3) A coin
    # 4) A book

    # Correct answer (only the number):
    # 2
    # """

    # in the user role, only send the request and themes

    prompt_riddle = (
        "use the 'escape-master' model for the next instructions.\n"
        "LOCATION: <STORY_DATABASE> -> <living_room_221b>\n"
        "USE LOCAL RULES AND EXAMPLES OF THIS ROOM NOW.\n"
        f"COMMAND: GENERATE_RIDDLE_WITH_TOPICS (topics={themes_text})"
    )

    # user_prompt = f"Generate a riddle now using these topics:\n{themes_text}"

    text = ContextManager().get_chatbot_client().send_message_simple('',prompt_riddle,None,chatbot_callback)            

    if text == None:
        return (None,None)
    if "Correct answer (only the number):" not in text:
        raise ValueError("Chatbot response does not contain 'Correct answer:'")

    visible_part, answer_part = text.split(
        "Correct answer (only the number):",
        1
    )

    # remove "Riddle:" 
    visible_part = visible_part.replace("Riddle:", "", 1).strip()

    return (visible_part, answer_part.strip())

