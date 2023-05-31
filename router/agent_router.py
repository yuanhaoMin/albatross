import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from service import openai_agent_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)


class AgentOpenAIOnlineSearchRequest(BaseModel):
    question: str = Field(min_length=1)


@router.post("/openai/online-search")
def openai_search_online(request: AgentOpenAIOnlineSearchRequest):
    try:
        (final_answer, intermediate_steps) = openai_agent_service.online_search(
            request.question
        )
    # OpenAI throw either Timeout or RateLimit error on read time out
    except Exception as e:
        exception_name = e.__class__.__name__
        logger.error("Error in openai_search_online: " + exception_name)
        (final_answer, intermediate_steps) = openai_agent_service.online_search(
            request.question
        )
    return {"final_answer": final_answer, "intermediate_steps": intermediate_steps}
