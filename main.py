import sys
sys.path.append("/opt/ml/input/level3_cv_finalproject-cv-11/deepfake")

from fastapi import FastAPI
import uvicorn

from backend.routers.user import users_router
from backend.routers.generation_file import generation_router
from backend.routers.inference import inference_router
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
# app.include_router(inference_router, tags=["inference"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=30007)