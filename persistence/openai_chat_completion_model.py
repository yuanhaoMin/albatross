from configuration.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP


class OpenAIChatCompletion(Base):
    __tablename__ = "openai_chat_completion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("app_user.id"))
    messages = Column(String)
    model = Column(String)
    temperature = Column(Float)
    update_time = Column(TIMESTAMP)
