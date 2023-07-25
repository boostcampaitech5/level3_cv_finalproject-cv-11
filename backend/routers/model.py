from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
# from database import Base
from backend.routers.database import Base

## users
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    hashed_password = Column(String, unique=True, index=True)
    signin_name = Column(String)

## 생성, 탐지 프로젝트 클래스
class UsersGeneration(Base):
    __tablename__ = "user_generation"

    user_id = Column(Integer, index=True)
    project_id = Column(Integer, primary_key=True)
    project_name = Column(String, index=True)

class UsersDetection(Base):
    __tablename__ = "user_detection"

    user_id = Column(Integer, index=True)
    project_id = Column(Integer, primary_key=True)
    project_name = Column(String, index=True)

class GenerationProject(Base):
    __tablename__ = "generation"

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    state = Column(String)
    

class DetectionProject(Base):
    __tablename__ = "detection"

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    output = Column(String)
    race = Column(Integer)
    gender = Column(Integer)
    age = Column(Integer)
    state = Column(String)
    rating = Column(Integer)

