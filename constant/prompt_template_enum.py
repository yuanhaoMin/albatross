from constant import prompt_template_content
from enum import Enum


class PromptTemplateEnum(Enum):
    NONE = (-1, "", {})
    DEFAULT = (0, prompt_template_content.default, {"question"})
    PDF_CHAT = (1, prompt_template_content.pdf_chat, {"pdf", "question"})
    RESUME_SCREENING = (
        10,
        prompt_template_content.resume_screening,
        {"pdf", "position_description"},
    )
    INTERVIEW_QUESTIONS = (
        12,
        prompt_template_content.interview_questions,
        {"requirement"},
    )
    BELBIN_TEAM_ROLES_POSITION_DESCRIPTION = (
        14,
        prompt_template_content.belbin_team_role_position_description,
        {"position_description"},
    )
    JAVA_RENAME = (30, prompt_template_content.java_rename, {"description", "code"})

    def __init__(self, id: int, template: str, arg_names: list[str]):
        self.id = id
        self.template = template
        self.arg_names = arg_names

    @classmethod
    def from_id(cls, id) -> "PromptTemplateEnum":
        for item in cls:
            if item.id == id:
                return item
        raise ValueError(f"No prompt template with id {id} found")
