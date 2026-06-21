from fastapi import APIRouter, HTTPException
from schemas import VoiceRequest, VoiceResponse
from services.voice_service import create_voice

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/generate", response_model=VoiceResponse)
def create_voice_route(payload: VoiceRequest):
    try:
        audio_path = create_voice(payload.text)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return VoiceResponse(audio_path=audio_path)
