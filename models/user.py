from sqlalchemy import Boolean, Column, Integer, String, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    birthday = Column(DateTime)
    age = Column(Integer, )
    password = Column(String)
    confirm_password = Column(String)
    created_at = Column(DateTime)
