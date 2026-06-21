from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    category = Column(String)  # e.g. "AI/Tech", "Fitness", etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReelProject(Base):
    """Tracks each reel generation job through the pipeline."""
    __tablename__ = "reel_projects"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=True)

    topic = Column(String)
    script = Column(Text, nullable=True)
    audio_path = Column(String, nullable=True)
    image_paths = Column(Text, nullable=True)  # comma-separated or JSON string
    video_path = Column(String, nullable=True)

    status = Column(String, default="pending")  # pending|script_done|voice_done|images_done|video_done|failed
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
