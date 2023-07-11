from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from routers.user import users_router
from routers.file import file_router
from fastapi.middleware.cors import CORSMiddleware

# from app.api.api_v1.routers.auth import auth_router
# from app.core import config
# from app.db.session import SessionLocal
# from app.core.auth import get_current_active_user
# from app.core.celery_app import celery_app
# from app import tasks

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, tags=["users"])
app.include_router(file_router, tags=["file"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)