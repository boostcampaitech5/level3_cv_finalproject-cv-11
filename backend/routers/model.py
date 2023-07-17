from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
# from database import Base
from backend.routers.database import Base

## users
class User(Base):
    __tablename__ = "users"

    # user_id = Column(Integer, primary_key=True)
    username = Column(String, index=True, primary_key=True)      #식별자라는데 정확히는 모르겠다
    hashed_password = Column(String, unique=True, index=True)
    signin_name = Column(String)

## 생성, 탐지 프로젝트 클래스 지정
class GenerationProject(Base):
    __tablename__ = "generation"

    project_id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    project_name = Column(String, index=True)
    state = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    output_url = Column(String)

class DetectionProject(Base):
    __tablename__ = "detection"

    project_id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    project_name = Column(String, index=True)
    state = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    output_url = Column(String)

