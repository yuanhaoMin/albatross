from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from schema.openai_completion_schema import (
    UpdateCompletionRequest,
    UpdateCompletionResponse,
)
from schema.openai_chat_completion_schema import (
    UpdateChatCompletionRequest,
    UpdateChatCompletionResponse,
)
from service.openai_completion_service import (
    create_update_completion,
    generate_completion_stream,
    generate_test_stream,
    prepare_completion,
)
from service.openai_chat_completion_service import (
    create_update_chat_completion,
    delete_user_chat_completions,
    delete_chat_completion,
    generate_chat_completion_stream,
    prepare_chat_completion,
)
from sqlalchemy.orm import Session
from util.db_util import get_db


router = APIRouter(
    prefix="/llm/openai",
    tags=["llm openai"],
    responses={404: {"description": "Not found"}},
)


@router.get("/chat-completion-stream", response_class=StreamingResponse)
def chat_with_stream(
    chat_completion_id: int, test_mode: bool, db: Session = Depends(get_db)
):
    chat_completion, chat_model, messages, db = prepare_chat_completion(
        chat_completion_id, db
    )
    if test_mode:
        return StreamingResponse(
            generate_test_stream(str(messages)),
            media_type="text/event-stream",
        )
    else:
        return StreamingResponse(
            generate_chat_completion_stream(chat_completion, chat_model, messages, db),
            media_type="text/event-stream",
        )


@router.get("/completion-stream", response_class=StreamingResponse)
def complete_with_stream(
    completion_id: int, test_mode: bool, db: Session = Depends(get_db)
):
    llm, prompt = prepare_completion(completion_id, db)
    if test_mode:
        return StreamingResponse(
            generate_test_stream(prompt),
            media_type="text/event-stream",
        )
    else:
        return StreamingResponse(
            generate_completion_stream(llm, prompt),
            media_type="text/event-stream",
        )


@router.delete("/chat-completion")
def reset_user_chat_completions(username: str, db: Session = Depends(get_db)):
    return delete_user_chat_completions(username, db)


@router.delete("/chat-completion/{chat_completion_id}")
def reset_chat_completion(chat_completion_id: int, db: Session = Depends(get_db)):
    return delete_chat_completion(chat_completion_id, db)


@router.put("/chat-completion", response_model=UpdateChatCompletionResponse)
def update_chat_completion(
    request: UpdateChatCompletionRequest,
    db: Session = Depends(get_db),
):
    return create_update_chat_completion(request, db)


@router.put("/completion", response_model=UpdateCompletionResponse)
def update_completion(
    request: UpdateCompletionRequest,
    db: Session = Depends(get_db),
):
    return create_update_completion(request, db)
