from fastapi import APIRouter
from pydantic import BaseModel
from service import openai_image

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)


class ImageOpenAIGenerationRequest(BaseModel):
    prompt: str
    n: int
    size: str


@router.post("/openai/generation")
async def openai_generate_images(request: ImageOpenAIGenerationRequest):
    return openai_image.generate_images(request.prompt, request.n, request.size)
