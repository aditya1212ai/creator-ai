from google import genai
from config import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY missing. Set it in your .env file.")
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def generate_script(topic: str, tone: str = "casual Hinglish, skeptical and direct") -> str:
    """
    Generates a viral reel script: Hook / Body / CTA.
    Uses Gemini (free tier) instead of OpenAI.
    Raises RuntimeError on API failure so the route layer can convert it
    to a proper HTTP error instead of crashing silently.
    """
    prompt = f"""You are writing a short-form video script (Instagram Reel / YouTube Short).

Topic: {topic}
Tone: {tone}

Structure the script EXACTLY like this, with clear labels:

HOOK: (1-2 lines, must grab attention in first 3 seconds)
BODY: (3-5 short lines, deliver the core value/info)
CTA: (1 line, tell viewer exactly what to do — save, follow, comment)

Keep it punchy. No fluff. Write for someone scrolling fast."""

    client = _get_client()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
    except Exception as e:
        raise RuntimeError(f"Script generation failed: {e}")

    content = response.text
    if not content:
        raise RuntimeError("Script generation returned empty response")

    return content.strip()
    
