import sys
sys.path.append("routers/")

from fastapi import FastAPI, Depends
from starlette.requests import Request
import uvicorn

from routers.user import users_router
from routers.generation_file import generation_router
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
app.include_router(generation_router, tags=["generation_file"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=30008)