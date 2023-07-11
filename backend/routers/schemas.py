from typing import List, Optional
from pydantic import BaseModel



class UserBase(BaseModel):      #pydantic의 모델
    email: str


class UserCreate(UserBase):
    hashedpassword: str


#전반적인 flow는 위부터 흐르는 거라 보면됨
#pydantic: email을 통해 생성
#Usercreate는 이를 기반으로 db정보를 받아롤 수 있음
#이를 기반으로 User 모델 생성 그리고 이를 받고 싶으면 다시 pydantic을 써라? ->이건 진짜 모르겠다


class User(UserBase):           #sqlalchemy의 모델
    username: str
    # is_active: bool
    # items: List[Item] = []

    class Config:
        orm_mode = True