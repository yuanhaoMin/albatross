import asyncio
import json
from configuration.constant import APIKey
from fastapi import HTTPException
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
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
    update_time = get_current_berlin_time()
    print(request.prompt.encode("utf-8"))
    if user.completion is None:
        return openai_completion_crud.create_completion(
            user_id=user.id,
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )
    else:
        return openai_completion_crud.update_completion(
            completion_to_update=user.completion,
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )


def prepare_completion(username: str, db: Session) -> Tuple[OpenAI, str]:
    user = user_service.get_user_by_username(username, db)
    completion = user.completion
    llm = OpenAI(
        model_name=completion.model,
        temperature=completion.temperature,
        openai_api_key=APIKey.OPENAI_API_KEY,
        request_timeout=2,
        max_retries=1,
        streaming=True,
    )
    llm.max_tokens = llm.max_tokens_for_prompt(completion.prompt)
    return (llm, completion.prompt)


def generate_completion_stream(llm: OpenAI, prompt: str) -> str:
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
