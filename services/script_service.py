from openai import OpenAI
from config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_script(topic: str, tone: str = "casual Hinglish, skeptical and direct") -> str:
    """
    Generates a viral reel script: Hook / Body / CTA.
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
    except Exception as e:
        raise RuntimeError(f"Script generation failed: {e}")

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Script generation returned empty response")

    return content.strip()
