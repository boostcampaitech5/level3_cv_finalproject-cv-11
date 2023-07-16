import sys
sys.path.append("/opt/ml/level3_cv_finalproject-cv-11/deepfake")

from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from backend.routers.user import users_router
from backend.routers.file import file_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, tags=["users"])
app.include_router(file_router, tags=["file"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=30008)