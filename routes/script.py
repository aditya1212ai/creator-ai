from fastapi import APIRouter, HTTPException
from schemas import ScriptRequest, ScriptResponse
from services.script_service import generate_script

router = APIRouter(prefix="/script", tags=["script"])


@router.post("/generate", response_model=ScriptResponse)
def create_script(payload: ScriptRequest):
    try:
        script = generate_script(payload.topic, payload.tone)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return ScriptResponse(script=script)
