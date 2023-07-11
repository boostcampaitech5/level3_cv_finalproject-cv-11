from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import uvicorn

from passlib.context import CryptContext

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

templates = Jinja2Templates(directory='./')


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "88c2a56e0d8fc664a5d89fc7a9ade75b118beb5beacd317e54d4841b4926570e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

users_router = APIRouter()
# manager = LoginManager(
#     # here we set the secret LoginManager uses to encrypt our Token
#     # normally you would use Environment Variables or some kind of config
#     # where you can store the secret
#     secret="your-secret",
#     # We also have to set the tokenUrl, which is used to register the URL
#     # in the OpenAPI docs.
#     # This should be the same URL the user uses to login to your Application
#     tokenUrl="/auth/login"
#    )

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",      #secret
        "disabled": False,
    }
}

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]



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



def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request):   #, token: str = Depends(oauth2_scheme)
    token: str = request.cookies.get("access_token")
    if token is None:
        return None
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@users_router.get("/")
def get_login_form(request: Request):
    return templates.TemplateResponse('login_form.html', context={'request': request})

@users_router.get("/test")
def get_login_form(request: Request):
    token: str = request.cookies.get("access_token")
    return templates.TemplateResponse('login_form.html', context={'request': request})



@users_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = RedirectResponse("/users/me", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


@users_router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@users_router.get("/protected")
async def protected_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a protected endpoint"}

@users_router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


# if __name__ == '__main__':
#     uvicorn.run(users_router, host="0.0.0.0", port=8000)