from gtts import gTTS
import os
from config import settings


def create_voice(text: str, output_filename: str = "voice.mp3") -> str:
    """
    Generates Hindi/Hinglish voiceover using gTTS (free, no API key needed).
    """
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(settings.OUTPUT_DIR, output_filename)

    try:
        tts = gTTS(text=text, lang='hi', slow=False)
        tts.save(output_path)
    except Exception as e:
        raise RuntimeError(f"Voice generation failed: {e}")

    return output_path
