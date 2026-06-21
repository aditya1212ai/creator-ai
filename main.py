import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import init_db
from config import settings
from routes import script, voice, image, video, pipeline

app = FastAPI(title="CreatorAI", version="0.1.0")

# Serve generated videos/images/audio so the frontend can preview & download them
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=settings.OUTPUT_DIR), name="outputs")

# Flutter app will hit this from a different origin during dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your actual app domain before production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(script.router)
app.include_router(voice.router)
app.include_router(image.router)
app.include_router(video.router)
app.include_router(pipeline.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def health_check():
    return {"status": "ok", "service": "CreatorAI backend"}
