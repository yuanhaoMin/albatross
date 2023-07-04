from persistence.openai_completion_model import OpenAICompletion
from sqlalchemy.orm import Session
from util.time_util import get_current_utc8_time


def create_completion(
    user_id: int,
    prompt: str,
    template_id: int,
    template_args: str,
    model: str,
    temperature: float,
    db: Session,
) -> OpenAICompletion:
    completion = OpenAICompletion(
        user_id=user_id,
        prompt=prompt,
        template_id=template_id,
        template_args=template_args,
        model=model,
        temperature=temperature,
        update_time=get_current_utc8_time(),
        usage_count=1,
    )
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
    usage_count: int,
    db: Session,
) -> OpenAICompletion:
    completion_to_update.prompt = prompt
    completion_to_update.template_id = template_id
    completion_to_update.template_args = template_args
    completion_to_update.model = model
    completion_to_update.temperature = temperature
    completion_to_update.update_time = get_current_utc8_time()
    completion_to_update.usage_count = usage_count
    db.commit()
    db.refresh(completion_to_update)
    return completion_to_update
