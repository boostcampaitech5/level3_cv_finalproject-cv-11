from pydantic import BaseModel, Field
from datetime import datetime

class UserId(BaseModel):
    id: int

class UserBase(BaseModel):
    signin_name: str

class UserCreate(UserBase):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")

class User(UserBase):
    username: str

    class Config:
        orm_mode = True

class ProjectIdCreate(BaseModel):
    user_id: int = Field(..., description="User id of the user")
    project_name: str = Field(..., description="Creation time of the project")

class ProjectCreate(BaseModel):
    project_name: str = Field(..., description="Creation time of the project")
    state: str = Field(..., description="Learning-state of the project")
    start_time: datetime = Field(..., description="Start time of the project")

class GenerationProject(ProjectCreate):
    end_time: datetime = Field(..., description="End time of the project")

class DetectionProject(ProjectCreate):
    output: str = Field(..., description="Output of the project")
    race: int = Field(..., description="Person info of the project")
    gender: int = Field(..., description="Person info of the project")
    age: int = Field(..., description="Person info of the project")
    rating: int = Field(..., description="Rating of the project")
