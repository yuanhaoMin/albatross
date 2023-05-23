from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from schema import openai_completion_schema
from service import openai_completion_service
from sqlalchemy.orm import Session
from util.db_util import get_db


router = APIRouter(
    prefix="/completion/openai",
    tags=["completion openai"],
    responses={404: {"description": "Not found"}},
)


@router.get("/completion-stream", response_class=StreamingResponse)
def complete_with_stream(username: str, test_mode: bool, db: Session = Depends(get_db)):
    llm, prompt = openai_completion_service.prepare_completion_with_stream(username, db)
    if test_mode:
        return StreamingResponse(
            openai_completion_service.generate_test_stream(prompt),
            media_type="text/event-stream",
        )
    else:
        return StreamingResponse(
            openai_completion_service.generate_completion_stream(llm, prompt),
            media_type="text/event-stream",
        )


@router.post(
    "/update", response_model=openai_completion_schema.UpdateCompletionResponse
)
def update_completion(
    request: openai_completion_schema.UpdateCompletionRequest,
    db: Session = Depends(get_db),
):
    return openai_completion_service.update_completion(request, db)
