from fastapi import APIRouter, HTTPException
from schemas import ImageRequest, ImageResponse
from services.image_service import generate_images

router = APIRouter(prefix="/image", tags=["image"])


@router.post("/generate", response_model=ImageResponse)
def create_images_route(payload: ImageRequest):
    try:
        images = generate_images(payload.script, payload.num_scenes)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return ImageResponse(images=images)
