from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from database import get_db
from models import ReelProject
from services.script_service import generate_script
from services.voice_service import create_voice
from services.image_service import generate_images

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


class FullPipelineRequest(BaseModel):
    topic: str
    num_scenes: Optional[int] = 3


class FullPipelineResponse(BaseModel):
    project_id: int
    script: str
    audio_path: str
    image_paths: List[str]
    status: str


@router.post("/generate-reel", response_model=FullPipelineResponse)
def generate_reel(payload: FullPipelineRequest, db: Session = Depends(get_db)):
    project = ReelProject(topic=payload.topic, status="pending")
    db.add(project)
    db.commit()
    db.refresh(project)

    try:
        script = generate_script(payload.topic)
        project.script = script
        project.status = "script_done"
        db.commit()

        audio_path = create_voice(script, output_filename=f"voice_{project.id}.mp3")
        project.audio_path = audio_path
        project.status = "voice_done"
        db.commit()

        image_paths = generate_images(script, payload.num_scenes)
        project.image_paths = ",".join(image_paths)
        project.status = "images_done"
        db.commit()

    except RuntimeError as e:
        project.status = "failed"
        project.error_message = str(e)
        db.commit()
        raise HTTPException(
            status_code=502,
            detail=f"Pipeline failed at stage '{project.status}': {e}",
        )

    return FullPipelineResponse(
        project_id=project.id,
        script=project.script,
        audio_path=f"/outputs/voice_{project.id}.mp3",
        image_paths=[f"/outputs/scene{i+1}.jpg" for i in range(len(image_paths))],
        status=project.status,
    )


@router.get("/status/{project_id}")
def get_pipeline_status(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ReelProject).filter(ReelProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "project_id": project.id,
        "topic": project.topic,
        "status": project.status,
        "error_message": project.error_message,
    }
