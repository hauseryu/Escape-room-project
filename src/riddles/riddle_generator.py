from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
THEMES_FILE = BASE_DIR / "themes.txt"

with open(THEMES_FILE, "r", encoding="utf-8") as file:
    THEMES = [line.strip() for line in file if line.strip()]

selected_themes = random.sample(THEMES, 4)

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is not set. Please add it to your .env file.")

client = genai.Client(api_key=api_key)


def generate_riddle():
    selected_themes = random.sample(THEMES, 3)

    themes_text = ", ".join(selected_themes)

    config = types.GenerateContentConfig(
        max_output_tokens=200,
        temperature=1.0,
    )

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
            - The riddle should have a high difficulty level, but not too complex and specific.

            Answer exactly in this format:

            Riddle:
            ...

            A)
            B)
            C)
            D)

            Correct answer:
            ...
            """,
        config=config
    )

    return response.text
