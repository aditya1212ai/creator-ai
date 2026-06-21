from pydantic import BaseModel, Field
from typing import Optional, List


class ScriptRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    tone: Optional[str] = "casual Hinglish, skeptical and direct"


class ScriptResponse(BaseModel):
    script: str


class VoiceRequest(BaseModel):
    text: str = Field(..., min_length=2)
    project_id: Optional[int] = None


class VoiceResponse(BaseModel):
    audio_path: str


class ImageRequest(BaseModel):
    script: str
    num_scenes: Optional[int] = 3


class ImageResponse(BaseModel):
    images: List[str]


class VideoRequest(BaseModel):
    image_paths: List[str]
    audio_path: str
    project_id: Optional[int] = None


class VideoResponse(BaseModel):
    video_path: str


class FullPipelineRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    num_scenes: Optional[int] = 3


class FullPipelineResponse(BaseModel):
    project_id: int
    script: str
    audio_path: str
    image_paths: List[str]
    video_path: str
    status: str
