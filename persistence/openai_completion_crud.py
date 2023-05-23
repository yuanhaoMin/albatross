from datetime import datetime
from persistence.openai_completion_model import OpenAICompletion
from sqlalchemy.orm import Session


def create_update_completion(
    user_id: int,
    prompt: str,
    model: str,
    temperature: float,
    update_time: datetime,
    db: Session,
) -> OpenAICompletion:
    db_completion = (
        db.query(OpenAICompletion).filter(OpenAICompletion.user_id == user_id).first()
    )
    if db_completion is None:
        db_completion = OpenAICompletion(
            user_id=user_id,
            prompt=prompt,
            model=model,
            temperature=temperature,
            update_time=update_time,
        )
        db.add(db_completion)
    else:
        db_completion.prompt = prompt
        db_completion.model = model
        db_completion.temperature = temperature
        db_completion.update_time = update_time
    db.commit()
    db.refresh(db_completion)
    return db_completion


def get_completion_by_user_id(user_id: int, db: Session) -> OpenAICompletion:
    return (
        db.query(OpenAICompletion).filter(OpenAICompletion.user_id == user_id).first()
    )
