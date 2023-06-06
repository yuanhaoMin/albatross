from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from schema.template_args_schema import TemplateArgs
from typing import List


class ModelType(str, Enum):
    davinci_3 = "text-davinci-003"
    gpt_35 = "gpt-3.5-turbo"
    gpt_4 = "gpt-4"


class CompletionBase(BaseModel):
    model: ModelType
    temperature: float = Field(ge=0.0, le=2.0)


class UpdateCompletionRequest(CompletionBase):
    username: str
    template_id: int
    template_args: List[TemplateArgs]


class UpdateCompletionResponse(CompletionBase):
    id: int
    update_time: datetime

    class Config:
        orm_mode = True
