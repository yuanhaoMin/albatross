from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from service import openai_completion_service
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/completion",
    tags=["completion"],
    responses={404: {"description": "Not found"}},
)


@router.get("/openai/completion-stream")
async def openai_complete_with_stream(username: str):
    return StreamingResponse(
        openai_completion_service.complete_with_stream(username),
        media_type="text/event-stream",
    )
