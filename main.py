# gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
# uvicorn main:app --reload
import os
import sys
from fastapi import FastAPI, HTTPException
from io import StringIO
from pydantic import BaseModel
import service.agent_google_search as agent_google_search

app = FastAPI()


@app.get("/")
async def health_check():
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
