import asyncio
from langchain.llms import OpenAI
from persistence.openai_completion_crud import (
    create_completion,
    read_completion,
    update_completion,
)
from persistence.openai_completion_model import OpenAICompletion
from schema.event_data_schema import EventData
from schema.openai_completion_schema import UpdateCompletionRequest
from service.setting_service import get_api_key_settings
from service.user_service import get_user_by_username
from sqlalchemy.orm import Session
from typing import Tuple
from util.time_util import get_current_berlin_time


def create_update_completion(
    request: UpdateCompletionRequest, db: Session
) -> OpenAICompletion:
    user = get_user_by_username(request.username, db)
    update_time = get_current_berlin_time()
    if user.completion is None:
        return create_completion(
            user_id=user.id,
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )
    else:
        return update_completion(
            completion_to_update=user.completion,
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )


def prepare_completion(completion_id: int, db: Session) -> Tuple[OpenAI, str]:
    completion = read_completion(completion_id, db)
    llm = OpenAI(
        model_name=completion.model,
        temperature=completion.temperature,
        openai_api_key=get_api_key_settings().openai_api_key,
        request_timeout=2,
        max_retries=1,
        streaming=True,
    )
    llm.max_tokens = llm.max_tokens_for_prompt(completion.prompt)
    return (llm, completion.prompt)


def generate_completion_stream(llm: OpenAI, prompt: str) -> str:
    for stream_response in llm.stream(prompt):
        event_data = EventData()
        event_data.content = stream_response["choices"][0]["text"]
        finish_reason = stream_response["choices"][0]["finish_reason"]
        if finish_reason == "stop":
            event_data.hasEnd = True
            yield "data: %s\n\n" % event_data.json()
        else:
            yield "data: %s\n\n" % event_data.json()


async def generate_test_stream(text: str) -> str:
    event_data = EventData()
    for i in range(3):
        event_data.content = text
        yield "data: %s\n\n" % event_data.json()
        await asyncio.sleep(0.5)
    event_data.hasEnd = True
    yield "data: %s\n\n" % event_data.json()
