from persistence.openai_chat_completion_model import OpenAIChatCompletion
from sqlalchemy.orm import Session
from util.time_util import get_current_utc8_time


def create_chat_completion(
    user_id: int,
    messages: str,
    template_id: int,
    template_args: str,
    model: str,
    temperature: float,
    db: Session,
) -> OpenAIChatCompletion:
    chat_completion = OpenAIChatCompletion(
        user_id=user_id,
        messages=messages,
        template_id=template_id,
        template_args=template_args,
        model=model,
        temperature=temperature,
        update_time=get_current_utc8_time(),
        usage_count=1,
    )
    db.add(chat_completion)
    db.commit()
    db.refresh(chat_completion)
    return chat_completion


def delete_chat_completions(
    chat_completions: list[OpenAIChatCompletion],
    db: Session,
) -> None:
    for chat_completion in chat_completions:
        db.delete(chat_completion)
    db.commit()


def delete_chat_completion_by_id(
    chat_completion_id: int,
    db: Session,
) -> None:
    db.query(OpenAIChatCompletion).filter(
        OpenAIChatCompletion.id == chat_completion_id
    ).delete()
    db.commit()


def read_chat_completion_by_id(
    chat_completion_id: int,
    db: Session,
) -> OpenAIChatCompletion:
    return (
        db.query(OpenAIChatCompletion)
        .filter(OpenAIChatCompletion.id == chat_completion_id)
        .first()
    )


def update_chat_completion(
    chat_completion_to_update: OpenAIChatCompletion,
    messages: str,
    template_id: int,
    template_args: str,
    model: str,
    temperature: float,
    usage_count: int,
    db: Session,
) -> OpenAIChatCompletion:
    chat_completion_to_update.messages = messages
    chat_completion_to_update.template_id = template_id
    chat_completion_to_update.template_args = template_args
    chat_completion_to_update.model = model
    chat_completion_to_update.temperature = temperature
    chat_completion_to_update.update_time = get_current_utc8_time()
    chat_completion_to_update.usage_count = usage_count
    db.commit()
    db.refresh(chat_completion_to_update)
    return chat_completion_to_update


def update_chat_completion_messages(
    chat_completion_to_update: OpenAIChatCompletion,
    messages: str,
    db: Session,
) -> OpenAIChatCompletion:
    chat_completion_to_update.messages = messages
    db.commit()
    db.refresh(chat_completion_to_update)
    return chat_completion_to_update
