from datetime import datetime
from persistence.openai_chat_completion_model import OpenAIChatCompletion
from sqlalchemy.orm import Session


def create_chat_completion(
    user_id: int,
    messages: str,
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAIChatCompletion:
    db_completion = OpenAIChatCompletion(
        user_id=user_id,
        messages=messages,
        model=model,
        temperature=temperature,
        update_time=update_time,
    )
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion


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
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAIChatCompletion:
    chat_completion_to_update.messages = messages
    chat_completion_to_update.model = model
    chat_completion_to_update.temperature = temperature
    chat_completion_to_update.update_time = update_time
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
