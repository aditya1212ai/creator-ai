import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from config import settings


def create_video(images: list[str], audio: str, output_filename: str = "final_video.mp4") -> str:
    """
    Stitches images into a video synced to audio duration, exports MP4.

    NOTE: written for moviepy >= 2.0 API (`with_duration`/`with_audio`,
    top-level `from moviepy import ...`). If your installed moviepy is
    < 2.0, use `set_duration`/`set_audio` and `from moviepy.editor import *` instead.
    Check your version with: pip show moviepy
    """
    if not images:
        raise RuntimeError("No images provided to create_video")
    if not os.path.exists(audio):
        raise RuntimeError(f"Audio file not found: {audio}")

    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(settings.OUTPUT_DIR, output_filename)

    audio_clip = AudioFileClip(audio)
    # split total audio duration evenly across the images so video matches voiceover length
    per_image_duration = audio_clip.duration / len(images)

    clips = []
    for image_path in images:
        if not os.path.exists(image_path):
            raise RuntimeError(f"Image file not found: {image_path}")
        clip = ImageClip(image_path).with_duration(per_image_duration)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")
    final = final.with_audio(audio_clip)

    try:
        final.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
        )
    finally:
        audio_clip.close()
        for c in clips:
            c.close()
        final.close()

    return output_path
