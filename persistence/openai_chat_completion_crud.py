from datetime import datetime
from persistence.openai_chat_completion_model import OpenAIChatCompletion
from sqlalchemy.orm import Session


def create_chat_completion(
    user_id: int,
    history: str,
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAIChatCompletion:
    db_completion = OpenAIChatCompletion(
        user_id=user_id,
        history=history,
        model=model,
        temperature=temperature,
        update_time=update_time,
    )
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion


def update_completion(
    chat_completion_to_update: OpenAIChatCompletion,
    history: str,
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAIChatCompletion:
    chat_completion_to_update.history = history
    chat_completion_to_update.model = model
    chat_completion_to_update.temperature = temperature
    chat_completion_to_update.update_time = update_time
    db.commit()
    db.refresh(chat_completion_to_update)
    return chat_completion_to_update
