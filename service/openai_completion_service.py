import asyncio
import logging
from fastapi import HTTPException
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from openai.error import Timeout
from persistence.openai_chat_completion_crud import update_chat_completion_messages
from persistence.openai_completion_crud import (
    create_completion,
    read_completion,
    update_completion,
)
from persistence.openai_chat_completion_model import OpenAIChatCompletion
from persistence.openai_completion_model import OpenAICompletion
from schema.event_data_schema import EventData
from schema.openai_completion_schema import ModelType, UpdateCompletionRequest
from service.setting_service import get_api_key_settings
from service.user_service import get_user_by_username
from sqlalchemy.orm import Session
from typing import List, Tuple, Union
from util.time_util import get_current_berlin_time

logger = logging.getLogger(__name__)


def create_llm(
    model_type: ModelType, temperature: float, prompt: str
) -> Union[OpenAI, ChatOpenAI]:
    if model_type == ModelType.davinci_3:
        llm = OpenAI(
            model_name=model_type,
            temperature=temperature,
            openai_api_key=get_api_key_settings().openai_api_key,
            request_timeout=2,
            max_retries=1,
            streaming=True,
        )
        llm.max_tokens = llm.max_tokens_for_prompt(prompt=prompt)
        return llm
    else:
        if model_type == ModelType.gpt_35:
            request_timeout = 2
        elif model_type == ModelType.gpt_4:
            request_timeout = 3
        llm = ChatOpenAI(
            model_name=model_type,
            temperature=temperature,
            openai_api_key=get_api_key_settings().openai_api_key,
            request_timeout=request_timeout,
            max_retries=1,
            streaming=True,
        )
        # calculate max tokens left for completion
        messages_tokens = llm.get_num_tokens_from_messages(eval(prompt))
        max_size = OpenAI.modelname_to_contextsize(self=OpenAI, modelname=model_type)
        llm.max_tokens = max_size - messages_tokens - 50
        return llm


def create_update_completion(
    request: UpdateCompletionRequest, db: Session
) -> OpenAICompletion:
    user = get_user_by_username(request.username, db)
    update_time = get_current_berlin_time()
    if request.model == ModelType.davinci_3:
        prompt = request.prompt
    else:
        messages = [HumanMessage(content=request.prompt)]
        prompt = str(messages)
    if user.completion is None:
        return create_completion(
            user_id=user.id,
            prompt=prompt,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )
    else:
        return update_completion(
            completion_to_update=user.completion,
            prompt=prompt,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )


def prepare_completion(completion_id: int, db: Session) -> Tuple[OpenAI, str]:
    completion = read_completion(completion_id, db)
    llm = create_llm(
        model_type=completion.model,
        temperature=completion.temperature,
        prompt=completion.prompt,
    )
    return (llm, completion.prompt)


def generate_stream_for_chat_model(
    chat_completion: OpenAIChatCompletion,
    chat_model: ChatOpenAI,
    messages: List[BaseMessage],
    db: Session,
) -> str:
    message_dicts, params = chat_model._create_message_dicts(messages, stop=None)
    event_data = EventData()
    contents = []
    retry_count = 0
    # TODO: the langchain retry logic is not working, need to fix it
    while True:
        try:
            for stream_response in chat_model.completion_with_retry(
                messages=message_dicts, **params
            ):
                delta = stream_response["choices"][0]["delta"]
                finish_reason = stream_response["choices"][0]["finish_reason"]
                if hasattr(delta, "content"):
                    contents.append(delta.content)
                    event_data.content = delta.content
                    yield "data: %s\n\n" % event_data.json()
                if finish_reason == "stop":
                    full_response_text = "".join(contents)
                    messages.append(AIMessage(content=full_response_text))
                    if chat_completion is not None:
                        update_chat_completion_messages(
                            chat_completion_to_update=chat_completion,
                            messages=str(messages),
                            db=db,
                        )
                    # return the last message
                    event_data.hasEnd = True
                    yield "data: %s\n\n" % event_data.json()
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


def generate_stream_for_completion_model(llm: OpenAI, prompt: str) -> str:
    for stream_response in llm.stream(prompt):
        event_data = EventData()
        event_data.content = stream_response["choices"][0]["text"]
        finish_reason = stream_response["choices"][0]["finish_reason"]
        if finish_reason == "stop":
            event_data.hasEnd = True
            yield "data: %s\n\n" % event_data.json()
        else:
            yield "data: %s\n\n" % event_data.json()


def generate_stream(llm: Union[OpenAI, ChatOpenAI], prompt: str) -> str:
    if isinstance(llm, OpenAI):
        return generate_stream_for_completion_model(llm=llm, prompt=prompt)
    else:
        messages: List[BaseMessage] = eval(prompt)
        return generate_stream_for_chat_model(
            chat_completion=None, chat_model=llm, messages=messages, db=None
        )


async def generate_test_stream(text: str) -> str:
    event_data = EventData()
    for i in range(3):
        event_data.content = text
        yield "data: %s\n\n" % event_data.json()
        await asyncio.sleep(0.5)
    event_data.hasEnd = True
    yield "data: %s\n\n" % event_data.json()
