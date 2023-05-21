from configuration.constant import APIKey
from openai import Image


def generate_images(prompt: str, n: int, size: str):
    return Image.create(
        api_key=APIKey.OPENAI_API_KEY,
        prompt=prompt,
        n=n,
        size=size,
    )
