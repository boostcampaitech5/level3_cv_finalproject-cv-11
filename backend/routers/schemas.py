from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime



## user 생성
class UserId(BaseModel):      #pydantic의 모델
    id: int

class UserBase(BaseModel):      #pydantic의 모델
    signin_name: str

class UserCreate(UserBase):
    username: str = Field(..., description="Username of the user")
    signin_name: str = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")


#전반적인 flow는 위부터 흐르는 거라 보면됨
#pydantic: email을 통해 생성
#Usercreate는 이를 기반으로 db정보를 받아롤 수 있음
#이를 기반으로 User 모델 생성 그리고 이를 받고 싶으면 다시 pydantic을 써라? ->이건 진짜 모르겠다

class User(UserBase):           #sqlalchemy의 모델
    username: str

    class Config:
        orm_mode = True



## project 생성
class ProjectIdCreate(BaseModel):
    user_id : int = Field(..., description="User id of the user")
    project_name: str = Field(..., description="Creation time of the project")

class ProjectCreate(BaseModel):
    project_id: str = Field(..., description="Created id of the project")
    project_name: str = Field(..., description="Creation time of the project")
    state: str = Field(..., description="Learning-state of the project")
    start_time: datetime = Field(..., description="start time of the project")

class GenerationProject(ProjectCreate):
    project_id: int = Field(..., description="Created id of the project")
    project_name: str = Field(..., description="Creation time of the project")
    start_time: datetime = Field(..., description="start time of the project")
    end_time: datetime = Field(..., description="start time of the project")
    state: str = Field(..., description="Learning-state of the project")

class DetectionProject(ProjectCreate):
    project_id: int = Field(..., description="Created id of the project")
    project_name: str = Field(..., description="Creation time of the project")
    start_time: datetime = Field(..., description="start time of the project")
    end_time: datetime = Field(..., description="start time of the project")
    output : str = Field(..., description="output of the project")
    race: int = Field(..., description="person info of the project")
    gender: int = Field(..., description="person info of the project")
    age: int = Field(..., description="person info of the project")
    state: str = Field(..., description="Learning-state of the project")
    rating: int = Field(..., description="rating of the project")
