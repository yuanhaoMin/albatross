from configuration.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP


class OpenAICompletion(Base):
    __tablename__ = "openai_completion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("app_user.id"))
    prompt = Column(String)
    history = Column(String)
    model = Column(String)
    temperature = Column(Float)
    update_time = Column(TIMESTAMP)
