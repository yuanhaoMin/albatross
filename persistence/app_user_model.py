from configuration.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class AppUser(Base):
    __tablename__ = "app_user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    access_bitmap = Column(Integer, default=1)
    created_time = Column(DateTime)
    last_login_time = Column(DateTime)
