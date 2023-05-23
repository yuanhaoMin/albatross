import asyncio
import json
from configuration.constant import APIKey
from fastapi import HTTPException
from langchain import OpenAI
from openai.error import Timeout
from persistence import openai_completion_crud
from persistence.openai_completion_model import OpenAICompletion
from schema import openai_completion_schema
from service import user_service
from sqlalchemy.orm import Session
from typing import Tuple
from util.time_util import get_current_berlin_time


def update_completion(
    request: openai_completion_schema.UpdateCompletionRequest, db: Session
) -> OpenAICompletion:
    user = user_service.get_user_by_username(request.username, db)
    user_id = user.id
    update_time = get_current_berlin_time()
    return openai_completion_crud.create_update_completion(
        user_id=user_id,
        prompt=request.prompt,
        model=request.model,
        temperature=request.temperature,
        update_time=update_time,
        db=db,
    )


def prepare_completion_with_stream(username: str, db: Session) -> Tuple[OpenAI, str]:
    user = user_service.get_user_by_username(username, db)
    completion = openai_completion_crud.get_completion_by_user_id(user.id, db)
    llm = OpenAI(
        model_name=completion.model,
        temperature=completion.temperature,
        max_tokens=4000,
        openai_api_key=APIKey.OPENAI_API_KEY,
        request_timeout=2,
        max_retries=1,
        streaming=True,
    )
    return (llm, completion.prompt)


async def generate_completion_stream(llm: OpenAI, prompt: str) -> str:
    try:
        for stream_response in llm.stream(prompt):
            chunk_data = {"data": stream_response["choices"][0]["text"]}
            yield json.dumps(chunk_data)
    except Timeout:
        # TODO: cancel the stream when timeout
        raise HTTPException(status_code=504, detail="OpenAI read timeout")


async def generate_test_stream(text: str) -> str:
    for i in range(3):
        chunk_data = {"data": text}
        yield json.dumps(chunk_data)
        await asyncio.sleep(0.5)
