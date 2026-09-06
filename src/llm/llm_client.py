from google import genai
import os
from dotenv import load_dotenv
from pathlib import Path

LLM_DIR = Path(__file__).resolve().parent
BASE_DIR = LLM_DIR.parent.parent

class LlmClient:
    def __init__(self):
        load_dotenv(dotenv_path=BASE_DIR / ".env")
        api_key = os.getenv("API_KEY")

        use_env_for_llm_settings = os.getenv("USE_ENV_FOR_LLM_SETTINGS")

        if use_env_for_llm_settings == "True":    
            self.deactivate_llm = os.getenv("LLM")
        else:
            self.deactivate_llm = os.environ.get('LLM', 'OFF')
        self.client = genai.Client(api_key=api_key) if api_key else None
