import os
import sys
home_path = os.environ['HOME']
sys.path.append(f"{home_path}/level3_cv_finalproject-cv-11/deepfake")

from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from backend.routers.user import users_router
from backend.routers.project import project_router
from backend.routers.generation import generation_router
from backend.routers.detection import detection_router
from backend.routers.port import port_router
from backend.routers.vertex import vertex_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:3000",  # 클라이언트의 Origin을 여기에 추가
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, tags=["users"])
app.include_router(project_router, tags=["project"])
app.include_router(generation_router, tags=["generation"])
app.include_router(detection_router, tags=["detection"])
app.include_router(port_router, tags=["port"])
app.include_router(vertex_router, tags=["vertex"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=30007)