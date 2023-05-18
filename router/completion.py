from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from service import openai_completion

router = APIRouter(
    prefix="/completion",
    tags=["completion"],
    responses={404: {"description": "Not found"}},
)


@router.get("/openai/completion-stream")
async def openai_complete_with_stream(username: str):
    return StreamingResponse(
        openai_completion.complete_with_stream(username), media_type="text/event-stream"
    )
