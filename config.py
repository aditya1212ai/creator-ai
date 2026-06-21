"""
Centralized configuration. Loads from .env so no API keys are hardcoded.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./creatorai.db")

    # Where generated assets get written
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "outputs")

    def validate(self):
        missing = []
        if not self.ELEVENLABS_API_KEY:
            missing.append("ELEVENLABS_API_KEY")
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")
        if missing:
            print(f"[WARNING] Missing env vars: {', '.join(missing)}. "
                  f"Related features will fail until set in .env")


settings = Settings()
settings.validate()
