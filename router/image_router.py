from fastapi import APIRouter
from pydantic import BaseModel, Field
from service import openai_image_service

router = APIRouter(
    prefix="/image",
    tags=["image"],
    responses={404: {"description": "Not found"}},
)


class ImageOpenAIGenerationRequest(BaseModel):
    prompt: str = Field(min_length=1)
    n: int
    size: str


@router.post("/openai/generation")
def openai_generate_images(request: ImageOpenAIGenerationRequest):
    return openai_image_service.generate_images(request.prompt, request.n, request.size)
