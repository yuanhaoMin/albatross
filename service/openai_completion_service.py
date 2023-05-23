import asyncio
import json
from configuration.constant import APIKey
from langchain.llms import OpenAI
from persistence.openai_completion_crud import create_completion, update_completion
from persistence.openai_completion_model import OpenAICompletion
from schema.openai_completion_schema import UpdateCompletionRequest
from service.user_service import get_user_by_username
from sqlalchemy.orm import Session
from typing import Tuple
from util.time_util import get_current_berlin_time
from util.tokenizer_util import detokenize, tokenize_and_convert_to_json_string


def create_update_completion(
    request: UpdateCompletionRequest, db: Session
) -> OpenAICompletion:
    user = get_user_by_username(request.username, db)
    tokenized_prompt_json = tokenize_and_convert_to_json_string(
        request.model, request.prompt
    )
    update_time = get_current_berlin_time()
    if user.completion is None:
        return create_completion(
            user_id=user.id,
            prompt=tokenized_prompt_json,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )
    else:
        return update_completion(
            completion_to_update=user.completion,
            prompt=tokenized_prompt_json,
            model=request.model,
            temperature=request.temperature,
            update_time=update_time,
            db=db,
        )


def prepare_completion(username: str, db: Session) -> Tuple[OpenAI, str]:
    user = get_user_by_username(username, db)
    completion = user.completion
    tokenized_prompt = json.loads(completion.prompt)
    original_prompt = detokenize(completion.model, tokenized_prompt)
    max_size = OpenAI.modelname_to_contextsize(OpenAI, completion.model)
    max_tokens = max_size - len(tokenized_prompt)
    llm = OpenAI(
        model_name=completion.model,
        temperature=completion.temperature,
        max_tokens=max_tokens,
        openai_api_key=APIKey.OPENAI_API_KEY,
        request_timeout=2,
        max_retries=1,
        streaming=True,
    )
    return (llm, original_prompt)


def generate_completion_stream(llm: OpenAI, prompt: str) -> str:
    for stream_response in llm.stream(prompt):
        chunk_data = {"data": stream_response["choices"][0]["text"]}
        yield json.dumps(chunk_data)


async def generate_test_stream(text: str) -> str:
    for i in range(3):
        chunk_data = {"data": text}
        yield json.dumps(chunk_data)
        await asyncio.sleep(0.5)
