import os
import requests
from config import settings


def _extract_keywords(script: str) -> str:
    """Extract a simple search keyword from the script topic."""
    # Remove labels and take first meaningful words
    import re
    cleaned = re.sub(r"(HOOK|BODY|CTA):", "", script, flags=re.IGNORECASE)
    words = cleaned.split()[:4]
    return " ".join(words)


def generate_images(script: str, num_scenes: int = 3) -> list[str]:
    """
    Fetches relevant stock images from Pexels based on script content.
    Free, no billing required.
    """
    if not settings.PEXELS_API_KEY:
        raise RuntimeError("PEXELS_API_KEY missing. Set it in your .env file.")

    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

    keyword = _extract_keywords(script)
    headers = {"Authorization": settings.PEXELS_API_KEY}

    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params={"query": keyword, "per_page": num_scenes, "orientation": "portrait"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(f"Pexels image fetch failed: {e}")

    photos = data.get("photos", [])
    if not photos:
        raise RuntimeError(f"No images found for keyword: {keyword}")

    image_paths = []
    for idx, photo in enumerate(photos[:num_scenes], start=1):
        img_url = photo["src"]["portrait"]
        img_response = requests.get(img_url, timeout=60)
        out_path = os.path.join(settings.OUTPUT_DIR, f"scene{idx}.jpg")
        with open(out_path, "wb") as f:
            f.write(img_response.content)
        image_paths.append(out_path)

    return image_paths
