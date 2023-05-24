from datetime import datetime
from persistence.openai_completion_model import OpenAICompletion
from sqlalchemy.orm import Session


def create_completion(
    user_id: int,
    prompt: str,
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAICompletion:
    db_completion = OpenAICompletion(
        user_id=user_id,
        prompt=prompt,
        model=model,
        temperature=temperature,
        update_time=update_time,
    )
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion


def read_completion(completion_id: int, db: Session) -> OpenAICompletion:
    return (
        db.query(OpenAICompletion).filter(OpenAICompletion.id == completion_id).first()
    )


def update_completion(
    completion_to_update: OpenAICompletion,
    prompt: str,
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAICompletion:
    completion_to_update.prompt = prompt
    completion_to_update.model = model
    completion_to_update.temperature = temperature
    completion_to_update.update_time = update_time
    db.commit()
    db.refresh(completion_to_update)
    return completion_to_update
