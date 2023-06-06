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

# Do not delete TemplateArgs, It is needed implicitly when eval messages
from schema.template_args_schema import TemplateArgs
from service.openai_completion_service import create_llm
from service.prompt_template_service import generate_prompt_from_template
from service.user_service import get_user_by_username
from sqlalchemy.orm import Session
from typing import List, Tuple, Type
from util.time_util import get_current_berlin_time

logger = logging.getLogger(__name__)


def create_update_chat_completion(
    request: UpdateChatCompletionRequest, db: Session
) -> OpenAIChatCompletion:
    user = get_user_by_username(request.username, db)
    chat_completion_to_update: Type[OpenAIChatCompletion] = next(
        (c for c in user.chat_completions if c.template_id == request.template_id),
        None,
    )
    if chat_completion_to_update is None:
        existing_args = []
    else:
        existing_args = eval(chat_completion_to_update.template_args)
    update_time = get_current_berlin_time()
    if not chat_completion_to_update:
        messages = []
        # User want custimized system message
        if request.system_message:
            system_message_content = request.system_message
        # User want to use template
        else:
            system_message_content = generate_prompt_from_template(
                template_id=request.template_id,
                existing_args=existing_args,
                new_args=request.template_args,
            )
        messages.append(
            SystemMessage(
                content=system_message_content,
            )
        )
        messages.append(HumanMessage(content=request.user_message))
        chat_completion = OpenAIChatCompletion(
            user_id=user.id,
            messages=str(messages),
            template_id=request.template_id,
            template_args=str(existing_args),
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
        )
        return create_chat_completion(chat_completion=chat_completion, db=db)
    else:
        history: Type[List[BaseMessage]] = eval(chat_completion_to_update.messages)
        # Last streaming is not successful
        if isinstance(history[-1], HumanMessage):
            # After refresh page, user may have different input
            history[-1].content = request.user_message
        else:
            history.append(HumanMessage(content=request.user_message))
        return update_chat_completion(
            chat_completion_to_update=chat_completion_to_update,
            messages=str(history),
            template_id=request.template_id,
            template_args=str(existing_args),
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


# TODO: add query parameter to filter by template_id
def get_user_template_chat_completion_history(
    username: str,
    template_id: int,
    db: Session,
) -> GetChatCompletionHistoryResponse:
    user = get_user_by_username(username, db)
    chat_completion: Type[OpenAIChatCompletion] = next(
        (c for c in user.chat_completions if c.template_id == template_id),
        None,
    )
    if not chat_completion:
        return GetChatCompletionHistoryResponse(
            id=-1,
            messages=[],
            update_time=None,
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
