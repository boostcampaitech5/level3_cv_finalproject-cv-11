from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# from database import Base
from backend.routers.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, index=True)      #식별자라는데 정확히는 모르겠다
    hashed_password = Column(String, unique=True, index=True)
    signin_name = Column(String)
