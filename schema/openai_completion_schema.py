from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ModelType(str, Enum):
    davinci_3 = "text-davinci-003"


class CompletionBase(BaseModel):
    model: ModelType
    temperature: float = Field(ge=0.0, le=2.0)


class UpdateCompletionRequest(CompletionBase):
    username: str
    prompt: str = Field(min_length=1)


class UpdateCompletionResponse(CompletionBase):
    id: int
    update_time: datetime

    class Config:
        orm_mode = True