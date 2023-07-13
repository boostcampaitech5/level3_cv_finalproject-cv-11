from typing import List, Optional
from pydantic import BaseModel, Field



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