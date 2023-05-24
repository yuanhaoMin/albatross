from pydantic import BaseModel, Field


class EventData(BaseModel):
    content: str = Field(default="")
    hasEnd: bool = Field(default=False)
