import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from openai.error import Timeout
from pydantic import BaseModel
from service import openai_agent

logger = logging.getLogger("agent-logger")

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)


class AgentOpenAIOnlineSearchRequest(BaseModel):
    question: str


@router.post("/openai/online-search")
async def openai_search_online(request: AgentOpenAIOnlineSearchRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question must not be empty")
    try:
        (final_answer, intermediate_steps) = openai_agent.online_search(
            request.question
        )
    except Timeout as e:
        logger.error("OpenAI API timeout, retrying...")
        (final_answer, intermediate_steps) = openai_agent.online_search(
            request.question
        )
    logger.info("final_answer: %s", final_answer)
    return {"final_answer": final_answer, "intermediate_steps": intermediate_steps}
