from datetime import datetime
from persistence.openai_completion_model import OpenAICompletion
from sqlalchemy.orm import Session


def create_completion(
    completion: OpenAICompletion,
    db: Session,
) -> OpenAICompletion:
    db.add(completion)
    db.commit()
    db.refresh(completion)
    return completion


def read_completion(completion_id: int, db: Session) -> OpenAICompletion:
    return (
        db.query(OpenAICompletion).filter(OpenAICompletion.id == completion_id).first()
    )


def update_completion(
    completion_to_update: OpenAICompletion,
    prompt: str,
    template_id: int,
    template_args: str,
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAICompletion:
    completion_to_update.prompt = prompt
    completion_to_update.template_id = template_id
    completion_to_update.template_args = template_args
    completion_to_update.model = model
    completion_to_update.temperature = temperature
    completion_to_update.update_time = update_time
    db.commit()
    db.refresh(completion_to_update)
    return completion_to_update
