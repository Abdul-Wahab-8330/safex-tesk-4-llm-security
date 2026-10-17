from functools import lru_cache

from google import genai

from .config import (
    API_KEY,
    MODEL_NAME,
    validate_configuration,
)


@lru_cache(maxsize=1)
def get_client():
    """Create and reuse one Gemini client."""
    validate_configuration()
    return genai.Client(api_key=API_KEY)


def generate_response(
    prompt,
    system_instruction,
    client=None,
    model_name=None,
):
    """Send a prompt to Gemini and return the generated text."""
    active_client = client or get_client()
    active_model = model_name or MODEL_NAME

    api_response = active_client.models.generate_content(
        model=active_model,
        contents=prompt,
        config={
            "system_instruction": system_instruction,
        },
    )

    return api_response.text or ""