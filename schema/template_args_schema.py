from pydantic import BaseModel


class TemplateArgs(BaseModel):
    name: str
    value: str
