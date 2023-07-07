from openai import Image
from service.setting_service import get_open_ai_api


def generate_images(prompt: str, n: int, size: str):
    return Image.create(
        api_key=get_open_ai_api(),
        prompt=prompt,
        n=n,
        size=size,
    )
