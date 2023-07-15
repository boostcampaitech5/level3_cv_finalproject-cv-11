from datetime import datetime, timedelta
from typing import Optional, Dict
# import crud, model, schemas
from backend.routers import crud, model, schemas


from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Form, Request, Response, Header
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates          #for debug
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
# from database import SessionLocal, engine
from backend.routers.database import SessionLocal, engine
from deepfake import make_synthesis, inference

from sqlalchemy.orm import Session


templates = Jinja2Templates(directory='./')             #for debug
model.Base.metadata.create_all(bind=engine)


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "88c2a56e0d8fc664a5d89fc7a9ade75b118beb5beacd317e54d4841b4926570e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)




def get_password_hash(password):
    return pwd_context.hash(password)



def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(request: Request):   #, token: str = Depends(oauth2_scheme)
#     token: str = request.cookies.get("access_token")
#     if token is None:
#         return None
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
@users_router.get("/generation")
def generation(request: Request):
    print('#########'*30)
    print(request.cookies.get('username'))
    source = f'/opt/ml/level3_cv_finalproject-cv-11/data/username/generation/{2}/source'
    target = f'/opt/ml/level3_cv_finalproject-cv-11/data/username/generation/{2}/target'
    output = f'/opt/ml/level3_cv_finalproject-cv-11/data/username/generation/{2}/result'
    make_synthesis.make_synthesis(target,source,output)
    return False

@users_router.get("/inference")
def inference_image():
    model_path = '/opt/ml/level3_cv_finalproject-cv-11/result/fewshot/Meta_train_learning_id_60.pt'
    real_path = '/opt/ml/level3_cv_finalproject-cv-11/data/username/detection/1/real'
    fake_path = '/opt/ml/level3_cv_finalproject-cv-11/data/username/detection/1/fake'
    target_path = '/opt/ml/level3_cv_finalproject-cv-11/data/username/detection/1/target'
    user_name = 'username'
    source = '/opt/ml/level3_cv_finalproject-cv-11/data/source'
    make_synthesis.make_synthesis(real_path,source,fake_path)
    result = inference.inference(model_path,real_path,fake_path,target_path,user_name)
    print(result)
    return result


@users_router.get("/")
def get_login_form(request: Request):
    print(request)
    print(f"cookie: {request._cookies}")

    print(f"request: {request.cookies.get('username')}")
    print(f"header: {request.headers}")
    print(f"body: {request.body}")
    print(f"json: {request.cookies}")
    client = request.client.host
    print(client)

    response = JSONResponse({'1':"2"})
    response.set_cookie(key="username", value="temp", httponly=False)

    print(response)
    return response


@users_router.post("/login")#, response_model=Token
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_for_login(db, username=form_data.username, password=form_data.password)
    # print(request.cookies)
    if not user:
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Incorrect username or password",
        #     headers={"WWW-Authenticate": "Bearer"},
        # )
        return {"islogin": False}
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = JSONResponse({'access_token':access_token})
    response.set_cookie(key="username", value=form_data.username, httponly=True, samesite="none")
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="none")         #maybe save access token to user_db
    # return response
    return {"islogin": True}


@users_router.post("/signin")
def create_user(signin_name: str = Form(...), username: str = Form(...),password: str=Form(...), db: Session = Depends(get_db)):          #Dict의 str, str은 key:str, value:str을 의미
    user_dict = {
        "username":username,
        "password":password,
        "signin_name":signin_name
    }
    print(user_dict)
    user = schemas.UserCreate(**user_dict)
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        # raise HTTPException(status_code=400, detail="Username already registered")
        return {"isvalid":False}
    # return crud.create_user(db=db, user=user)
    user = crud.create_user(db=db, user=user)
    # print(user)
    return {"isvalid":True}
