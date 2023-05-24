import logging
import json
from configuration.constant import APIKey
from fastapi import HTTPException
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from openai.error import Timeout
from persistence.openai_chat_completion_crud import (
    create_chat_completion,
    delete_chat_completions,
    delete_chat_completion_by_id,
    read_chat_completion_by_id,
    update_chat_completion,
    update_chat_completion_messages,
)
from persistence.openai_chat_completion_model import OpenAIChatCompletion
from schema.openai_chat_completion_schema import UpdateChatCompletionRequest
from service.user_service import get_user_by_username
from sqlalchemy.orm import Session
from typing import Tuple
from util.time_util import get_current_berlin_time

logger = logging.getLogger(__name__)


def create_update_chat_completion(
    request: UpdateChatCompletionRequest, db: Session
) -> OpenAIChatCompletion:
    user = get_user_by_username(request.username, db)
    update_time = get_current_berlin_time()
    if not len(user.chat_completions):
        messages = [
            SystemMessage(
                content=request.system_message,
            ),
            HumanMessage(content=request.user_message),
        ]
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
        chat_completion_to_update = user.chat_completions[-1]
        if chat_completion_to_update is None:
            raise HTTPException(
                status_code=400,
                detail=f"Chat completion with id {request.chat_completion_id} not found",
            )
        history = eval(chat_completion_to_update.messages)
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


def prepare_chat_completion(
    chat_completion_id: int, db: Session
) -> Tuple[OpenAIChatCompletion, ChatOpenAI, str, Session]:
    chat_completion = read_chat_completion_by_id(chat_completion_id, db)
    if chat_completion is None:
        raise HTTPException(
            status_code=400,
            detail=f"Chat completion with id {chat_completion_id} not found",
        )
    messages = eval(chat_completion.messages)
    # different models have different max_tokens
    request_timeout = 1.5
    if chat_completion.model == "gpt-4":
        request_timeout = 3
    chat_model = ChatOpenAI(
        model_name=chat_completion.model,
        temperature=chat_completion.temperature,
        openai_api_key=APIKey.OPENAI_API_KEY,
        request_timeout=request_timeout,
        max_retries=1,
        streaming=True,
    )
    # calculate max tokens left for completion
    messages_tokens = chat_model.get_num_tokens_from_messages(messages)
    max_size = OpenAI.modelname_to_contextsize(OpenAI, chat_completion.model)
    chat_model.max_tokens = max_size - messages_tokens
    return (chat_completion, chat_model, messages, db)


def generate_chat_completion_stream(
    chat_completion: OpenAIChatCompletion,
    chat_model: ChatOpenAI,
    messages: str,
    db: Session,
) -> str:
    message_dicts, params = chat_model._create_message_dicts(messages, stop=None)
    contents = []
    retry_count = 0
    # TODO: the langchain retry logic is not working, need to fix it
    while True:
        try:
            for stream_response in chat_model.completion_with_retry(
                messages=message_dicts, **params
            ):
                delta = stream_response.choices[0].delta
                finish_reason = stream_response.choices[0].finish_reason
                if hasattr(delta, "content"):
                    contents.append(delta.content)
                    chunk_data = {"data": delta.content}
                    yield json.dumps(chunk_data)
                if finish_reason == "stop":
                    full_response_text = "".join(contents)
                    messages.append(AIMessage(content=full_response_text))
                    update_chat_completion_messages(
                        chat_completion_to_update=chat_completion,
                        messages=str(messages),
                        db=db,
                    )
            break
        except Timeout:
            retry_count += 1
            if retry_count > chat_model.max_retries:
                raise HTTPException(
                    status_code=504,
                    detail=f"OpenAI API timeout after {chat_model.max_retries} retries",
                )
            else:
                logger.error("OpenAI API timeout, retrying...")
                continue
