import logging
from fastapi import HTTPException
from langchain.chat_models import ChatOpenAI, openai

# Do not delete AIMessage, It is needed implicitly when eval messages
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from persistence.openai_chat_completion_crud import (
    create_chat_completion,
    delete_chat_completions,
    delete_chat_completion_by_id,
    read_chat_completion_by_id,
    update_chat_completion,
)
from persistence.openai_chat_completion_model import OpenAIChatCompletion
from schema.openai_chat_completion_schema import (
    UpdateChatCompletionRequest,
    GetChatCompletionHistoryResponse,
)
from service.openai_completion_service import create_llm
from service.user_service import get_user_by_username
from sqlalchemy.orm import Session
from typing import List, Tuple, Type
from util.time_util import get_current_berlin_time

logger = logging.getLogger(__name__)


def create_update_chat_completion(
    request: UpdateChatCompletionRequest, db: Session
) -> OpenAIChatCompletion:
    user = get_user_by_username(request.username, db)
    update_time = get_current_berlin_time()
    if not len(user.chat_completions):
        messages = []
        if request.system_message:
            messages.append(
                SystemMessage(
                    content=request.system_message,
                )
            )
        messages.append(HumanMessage(content=request.user_message))
        return create_chat_completion(
            user_id=user.id,
            messages=str(messages),
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )
    else:
        # chat_completion_to_update = next(
        #     (c for c in user.chat_completions if c.id == request.chat_completion_id),
        #     None,
        # )
        # TODO: implement one user with multiple chat history
        chat_completion_to_update: Type[OpenAIChatCompletion] = user.chat_completions[
            -1
        ]
        if chat_completion_to_update is None:
            raise HTTPException(
                status_code=400,
                detail=f"Chat completion not found",
            )
        history: Type[list[BaseMessage]] = eval(chat_completion_to_update.messages)
        # last streaming is not successful
        if isinstance(history[-1], HumanMessage):
            # after refresh page, user may have different input
            history[-1].content = request.user_message
        else:
            history.append(HumanMessage(content=request.user_message))
        return update_chat_completion(
            chat_completion_to_update=chat_completion_to_update,
            messages=str(history),
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )


def delete_chat_completion(
    chat_completion_id: int,
    db: Session,
) -> None:
    delete_chat_completion_by_id(chat_completion_id, db)


def delete_user_chat_completions(
    username: str,
    db: Session,
) -> None:
    user = get_user_by_username(username, db)
    delete_chat_completions(user.chat_completions, db)


# TODO: implement one user with multiple chat history
def get_user_last_chat_completion_history(
    username: str,
    db: Session,
) -> GetChatCompletionHistoryResponse:
    user = get_user_by_username(username, db)
    chat_completion: Type[OpenAIChatCompletion] = user.chat_completions[-1]
    if chat_completion is None:
        raise HTTPException(
            status_code=400,
            detail=f"Chat completion not found",
        )
    messages = eval(chat_completion.messages)
    message_dicts = [openai._convert_message_to_dict(m) for m in messages]
    return GetChatCompletionHistoryResponse(
        id=chat_completion.id,
        messages=message_dicts,
        update_time=chat_completion.update_time,
    )


def prepare_chat_completion(
    chat_completion_id: int, db: Session
) -> Tuple[OpenAIChatCompletion, ChatOpenAI, List[BaseMessage]]:
    chat_completion = read_chat_completion_by_id(chat_completion_id, db)
    if chat_completion is None:
        raise HTTPException(
            status_code=400,
            detail=f"Chat completion with id {chat_completion_id} not found",
        )
    chat_model = create_llm(
        model_type=chat_completion.model,
        temperature=chat_completion.temperature,
        prompt=chat_completion.messages,
    )
    return (chat_completion, chat_model, eval(chat_completion.messages))
