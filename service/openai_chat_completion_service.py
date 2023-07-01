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
from service.filter_service import openai_check_harmful_content
from service.openai_completion_service import create_llm
from service.prompt_template_service import generate_prompt_from_template
from service.user_service import get_user_by_username
from sqlalchemy.orm import Session
from typing import List, Tuple, Type
from util.time_util import get_current_utc8_time


def create_update_chat_completion(
    request: UpdateChatCompletionRequest, db: Session
) -> OpenAIChatCompletion:
    # openai_check_harmful_content(request.user_message)

    user = get_user_by_username(request.username, db)
    chat_completion_to_update: Type[OpenAIChatCompletion] = next(
        (c for c in user.chat_completions if c.template_id == request.template_id),
        None,
    )
    existing_args = []
    messages = []
    update_time = get_current_utc8_time()
    if chat_completion_to_update is None:
        system_message = generate_system_message(request=request, existing_args=[])
        messages = [system_message, HumanMessage(content=request.user_message)]
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
        existing_args = eval(chat_completion_to_update.template_args)
        messages: Type[List[BaseMessage]] = eval(chat_completion_to_update.messages)
        if not messages:
            system_message = generate_system_message(request=request, existing_args=[])
            messages = [system_message, HumanMessage(content=request.user_message)]
        else:
            if isinstance(messages[-1], HumanMessage):
                # After refresh page, user may have different input
                messages[-1].content = request.user_message
            else:
                messages.append(HumanMessage(content=request.user_message))
        return update_chat_completion(
            chat_completion_to_update=chat_completion_to_update,
            messages=str(messages),
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
    # delete_chat_completions(user.chat_completions, db)
    reset_chat_completions(user.chat_completions, db)


def generate_system_message(
    request: UpdateChatCompletionRequest,
    existing_args: List[TemplateArgs],
) -> str:
    if request.system_message:
        system_message_content = request.system_message
    # User want to use template
    elif request.template_args:
        system_message_content = generate_prompt_from_template(
            template_id=request.template_id,
            existing_args=existing_args,
            new_args=request.template_args,
        )
    else:
        system_message_content = ""
    return SystemMessage(
        content=system_message_content,
    )


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
    messages: Type[List[BaseMessage]] = eval(chat_completion.messages)
    # Remove system message, which is the first message
    if messages and isinstance(messages[0], SystemMessage):
        messages = messages[1:]
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


def reset_chat_completions(
    chat_completions: List[OpenAIChatCompletion], db: Session
) -> None:
    for chat_completion in chat_completions:
        update_chat_completion(
            chat_completion_to_update=chat_completion,
            messages="[]",
            template_id=chat_completion.template_id,
            template_args=chat_completion.template_args,
            model=chat_completion.model,
            temperature=chat_completion.temperature,
            update_time=chat_completion.update_time,
            db=db,
        )
