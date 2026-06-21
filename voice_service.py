import os
import requests
from config import settings

ELEVENLABS_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def create_voice(text: str, output_filename: str = "voice.mp3") -> str:
    """
    Calls ElevenLabs TTS API and saves the audio file locally.
    Returns the path to the saved audio file.
    """
    if not settings.ELEVENLABS_API_KEY or not settings.ELEVENLABS_VOICE_ID:
        raise RuntimeError(
            "ElevenLabs API key or voice ID missing. Set ELEVENLABS_API_KEY "
            "and ELEVENLABS_VOICE_ID in your .env file."
        )

    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(settings.OUTPUT_DIR, output_filename)

    url = ELEVENLABS_TTS_URL.format(voice_id=settings.ELEVENLABS_VOICE_ID)
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # supports Hindi/Hinglish better than v1
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"ElevenLabs TTS request failed: {e}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
