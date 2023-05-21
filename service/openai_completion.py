import json
from configuration.database import SessionLocal
from persistence.app_user_schema import AppUserCreate
from persistence.app_user_crud import create_user
from configuration.constant import APIKey
from langchain import OpenAI


def complete_with_stream(username):
    # llm = OpenAI(
    #     model_name="text-davinci-003",
    #     temperature=0,
    #     max_tokens=4000,
    #     openai_api_key=APIKey.OPENAI_API_KEY,
    #     request_timeout=2,
    #     max_retries=1,
    #     streaming=True,
    # )
    # query = "Hi, how are you"
    # for resp in llm.stream(query):
    #     response = {"data": resp["choices"][0]["text"]}
    #     print(response)
    #     yield json.dumps(response)
    response = "Hi"
    app_user = AppUserCreate(
        username="your_username", password="your_password")
    create_user(SessionLocal, app_user=app_user)

    yield response
