import os
import re
from google import genai
from google.genai import types
from config import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY missing. Set it in your .env file.")
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _script_to_scene_prompts(script: str, num_scenes: int) -> list[str]:
    """
    Naive split of the HOOK/BODY/CTA script into N visual scene prompts.
    Strips the labels and breaks body into chunks if needed.
    """
    cleaned = re.sub(r"(HOOK|BODY|CTA):", "", script, flags=re.IGNORECASE)
    lines = [l.strip() for l in cleaned.splitlines() if l.strip()]

    if len(lines) >= num_scenes:
        step = len(lines) / num_scenes
        scenes = [lines[int(i * step)] for i in range(num_scenes)]
    else:
        # pad by repeating/cycling lines if script is too short
        scenes = (lines * num_scenes)[:num_scenes] if lines else ["Abstract tech background"] * num_scenes

    return [f"Vertical 9:16 cinematic illustration for a tech/AI reel: {s}" for s in scenes]


def generate_images(script: str, num_scenes: int = 3) -> list[str]:
    """
    Generates `num_scenes` images via Gemini and saves them locally.
    Returns list of file paths.
    """
    client = _get_client()
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

    prompts = _script_to_scene_prompts(script, num_scenes)
    image_paths = []

    for idx, prompt in enumerate(prompts, start=1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=prompt,
            )
        except Exception as e:
            raise RuntimeError(f"Gemini image generation failed for scene {idx}: {e}")

        saved = False
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                out_path = os.path.join(settings.OUTPUT_DIR, f"scene{idx}.png")
                with open(out_path, "wb") as f:
                    f.write(part.inline_data.data)
                image_paths.append(out_path)
                saved = True
                break

        if not saved:
            raise RuntimeError(f"Gemini returned no image data for scene {idx}")

    return image_paths
