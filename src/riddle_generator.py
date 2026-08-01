from google import genai
from google.genai import types 
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("API_KEY is not set. Please add it to your .env file.")


client = genai.Client(api_key=api_key)

config = types.GenerateContentConfig(
    max_output_tokens=200,       
)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite", 
    contents="Hallo Gemini! Erstelle mir ein kurzes Rätsel mit den Antworten und der richtigen Antwort.",
    config=config              
)

print(response.text)