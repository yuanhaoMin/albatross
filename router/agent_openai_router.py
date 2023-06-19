import logging
from fastapi import APIRouter
from pydantic import BaseModel, Field
from service import openai_agent_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/agent/openai",
    tags=["agent openai"],
    responses={404: {"description": "Not found"}},
)


class AgentOnlineSearchRequest(BaseModel):
    question: str = Field(min_length=1)


class AgentOnlineSearchResponse(BaseModel):
    final_answer: str


@router.post("/online-search", response_model=AgentOnlineSearchResponse)
def search_online(request: AgentOnlineSearchRequest) -> AgentOnlineSearchResponse:
    try:
        final_answer = openai_agent_service.online_search(request.question)
    # OpenAI throw either Timeout or RateLimit error on read time out
    except Exception as e:
        exception_name = e.__class__.__name__
        logger.error("Error in openai_search_online: " + exception_name)
        final_answer = openai_agent_service.online_search(request.question)
    return AgentOnlineSearchResponse(final_answer=final_answer)
