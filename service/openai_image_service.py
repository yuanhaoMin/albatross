from openai import Image
from service.setting_service import get_api_key_settings


def generate_images(prompt: str, n: int, size: str):
    return Image.create(
        api_key=get_api_key_settings().openai_api_key,
        prompt=prompt,
        n=n,
        size=size,
    )
