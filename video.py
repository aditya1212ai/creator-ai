from fastapi import APIRouter, HTTPException
from schemas import VideoRequest, VideoResponse
from services.video_service import create_video

router = APIRouter(prefix="/video", tags=["video"])


@router.post("/generate", response_model=VideoResponse)
def create_video_route(payload: VideoRequest):
    try:
        video_path = create_video(payload.image_paths, payload.audio_path)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return VideoResponse(video_path=video_path)
