from constant import prompt_template_content
from enum import Enum
from typing import List


class PromptTemplateEnum(Enum):
    DEFAULT = (0, prompt_template_content.default, {"question"})
    PDF_CHAT = (1, prompt_template_content.pdf_chat, {"pdf", "question"})

    def __init__(self, id: int, template: str, arg_names: List[str]):
        self.id = id
        self.template = template
        self.arg_names = arg_names

    @classmethod
    def from_id(cls, id) -> "PromptTemplateEnum":
        for item in cls:
            if item.id == id:
                return item
        raise ValueError(f"No prompt template with id {id} found")
