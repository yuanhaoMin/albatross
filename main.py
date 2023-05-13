# gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
# uvicorn main:app --reload
import logging
import requests
import sys
from fastapi import FastAPI, HTTPException
from io import StringIO
from openai.error import Timeout
from pydantic import BaseModel
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import service.agent_google_search as agent_google_search

logger = logging.getLogger("app-logger")
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,  # This is required
        allow_methods=["*"],
        allow_headers=["*"],
    )
]
app = FastAPI(middleware=middleware)


@app.get("/")
def health_check():
    return "Server is up!"


class AgentSearchRequest(BaseModel):
    question: str


@app.post("/agent-search")
def agent_search(request: AgentSearchRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question must not be empty")
    # Capture standard output in a string buffer
    stdout_buffer = StringIO()
    sys.stdout = stdout_buffer
    try:
        output, cost, total_tokens, successful_requests = agent_google_search.run(
            request.question
        )
    except Timeout as e:
        logger.error("OpenAI API timeout, retrying...")
        output, cost, total_tokens, successful_requests = agent_google_search.run(
            request.question
        )
    # Restore the standard output and get the captured string
    sys.stdout = sys.__stdout__
    captured_stdout = stdout_buffer.getvalue()
    return {
        "output": output,
        "metadata": {
            "cost": cost,
            "total_tokens": total_tokens,
            "successful_requests": successful_requests,
            "stdout": captured_stdout,
        },
    }


class ImagineGPTRequest(BaseModel):
    prompt: str
    n: int
    size: str


@app.post("/imagine-gpt")
def imagine(request: ImagineGPTRequest):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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",
    }
    data = {"prompt": request.prompt, "n": request.n, "size": request.size}
    response = requests.post(
        "https://api.openai.com/v1/images/generations", headers=headers, json=data
    )
    if response.status_code == 200:
        # Handle successful response
        result = response.json()
        # Process the result as needed
        return result
    else:
        # Handle error response
        raise HTTPException(status_code=response.status_code, detail=response.text)
