from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import ReelProject
from schemas import FullPipelineRequest, FullPipelineResponse
from services.script_service import generate_script
from services.voice_service import create_voice
from services.image_service import generate_images
from services.video_service import create_video

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/generate-reel", response_model=FullPipelineResponse)
def generate_reel(payload: FullPipelineRequest, db: Session = Depends(get_db)):
    """
    Runs the full pipeline: script -> voice -> images -> video.
    Persists progress to DB at each step so partial failures are visible
    and don't silently lose earlier work.
    """
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

        video_path = create_video(
            image_paths, audio_path, output_filename=f"reel_{project.id}.mp4"
        )
        project.video_path = video_path
        project.status = "video_done"
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
        audio_path=_to_url_path(project.audio_path),
        image_paths=[_to_url_path(p) for p in image_paths],
        video_path=_to_url_path(project.video_path),
        status=project.status,
    )


def _to_url_path(local_path: str) -> str:
    """Converts a local 'outputs/foo.mp4' path to a servable '/outputs/foo.mp4' URL path."""
    filename = local_path.split("/")[-1].split("\\")[-1]
    return f"/outputs/{filename}"


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
        "video_path": project.video_path,
    }
