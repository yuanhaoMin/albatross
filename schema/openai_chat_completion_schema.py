from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from schema.template_args_schema import TemplateArgs
from typing import Optional


class BaseMessage(BaseModel):
    role: str
    content: str


class ModelType(str, Enum):
    gpt_35 = "gpt-3.5-turbo"
    gpt_4 = "gpt-4"


class ChatCompletionBase(BaseModel):
    model: ModelType
    temperature: float = Field(ge=0.0, le=2.0)


class GetChatCompletionHistoryResponse(BaseModel):
    id: int
    messages: list[BaseMessage]
    update_time: datetime = None

    class Config:
        orm_mode = True


class UpdateChatCompletionRequest(ChatCompletionBase):
    username: str
    chat_completion_id: Optional[int] = None
    system_message: Optional[str] = ""
    user_message: str = Field(min_length=1)
    template_id: Optional[int] = -1
    template_args: Optional[list[TemplateArgs]] = []


class UpdateChatCompletionResponse(ChatCompletionBase):
    id: int
    update_time: datetime

    class Config:
        orm_mode = True
