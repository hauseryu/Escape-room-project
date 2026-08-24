from urllib import response

from google import genai
from google.genai import types
from google.genai import errors
import os
from dotenv import load_dotenv
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
THEMES_FILE = BASE_DIR / "themes.txt"

with open(THEMES_FILE, "r", encoding="utf-8") as file:
    THEMES = [line.strip() for line in file if line.strip()]

load_dotenv()

api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key) if api_key else None

def generate_riddle():
    selected_themes = random.sample(THEMES, 3)
    themes_text = ", ".join(selected_themes)

    config = types.GenerateContentConfig(
        max_output_tokens=200,
        temperature=1.0,
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
                Create a short riddle.

                Possible topics:
                {themes_text}

                Rules:
                - Use 2 to 3 of the given topics.
                - Maximum 2-3 short sentences.
                - Exactly one answer must be correct.
                - Do not use * or **.
                - The riddle should have a high difficulty level, but not too complex and specific.

                Answer exactly in this format:

                Riddle:
                ...

                1)
                2)
                3)
                4)

                Correct answer (only the number):
                ...
                """,
            config=config
        )
        
        text = response.text.strip()
    except errors.ServerError:
        text = "riddle currently not available!"

    if "Correct answer (only the number):" not in text:
        raise ValueError("LLM response does not contain 'Correct answer:'")

    visible_part, answer_part = text.split(
        "Correct answer (only the number):",
        1
    )

    # "Riddle:" entfernen
    visible_part = visible_part.replace("Riddle:", "", 1).strip()


    return (visible_part, answer_part.strip())
