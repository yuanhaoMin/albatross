from configuration.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class AppUser(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    access_bitmap = Column(Integer, default=1)
    created_time = Column(TIMESTAMP)
    last_login_time = Column(TIMESTAMP)
