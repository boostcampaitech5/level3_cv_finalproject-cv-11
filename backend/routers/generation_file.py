from typing import List, Dict
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse, FileResponse, Response
import os
import time
import base64
# from PIL import Image

generation_router = APIRouter()

fake_users_db = {
    "johndoe": {
        'user_id' : 1,
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",      #secret
        "disabled": False,
    }
}

# 폴더 생성
def make_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        return ('Error: Creating directory. ' +  path)
    
# 폴더 삭제
def delete_folder(path):
    try:
        if not os.path.exists(path):
            os.remove(path)
    except OSError:
        return ('Error: not exists directory. ' +  path)

# 생성하기 서비스 시간 생성
@generation_router.post("/generate/start")
async def create_generation():#usernames : str):
    username = 'johndoe1'
    project_name = time.strftime("%y%m%d%H%M%S", time.localtime())
    user_directory = f'../data/generate/{username}/{project_name}'
    make_folder(user_directory)
    return {'username': username, 'project_name' : project_name, "message": f"start generation."}

# 생성하기 서비스 삭제
@generation_router.post("/generate/calcel")
async def create_generation():#usernames : str, project_name : str):
    username = 'johndoe1'
    project_name = '230712150553'
    user_directory = f'../data/generate/{username}/{project_name}'
    delete_folder(user_directory)
    return {'username': username, 'project_name' : project_name, "message": f"project {project_name} delete."}


# 생성하기 이미지 업로드
@generation_router.post("/generate/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_files(project_name : str, files: List[UploadFile] = File(...)): #usernames : str):
    username = 'johndoe1'

    # 파일 수 확인 
    if len(files) != 2:
        return {"message": "정확히 2개의 이미지를 업로드해주세요."}

    # source, target 순으로 파일 저장
    service_directory = f'../data/generate/{username}/{project_name}'
    source_path = os.path.join(service_directory, 'sourch.jpeg')
    target_path = os.path.join(service_directory, 'sourch.jpeg')

    # 파일 저장
    with open(source_path, "wb") as buffer:
        buffer.write(await files[0].read())

    # 파일 저장
    with open(target_path, "wb") as buffer:
        buffer.write(await files[1].read())
    
    return {"message": f"File uploaded successfully."}


# generation 프로젝트 리스트 조회
@generation_router.get("/generate/projects")
async def generation_project_list():
    username = 'johndoe1'
    service_directory = f'../data/generation/{username}'
    project_list = os.listdir(service_directory)
    return {"username": username, "project_list": project_list}

# 프로젝트 내 이미지 리스트 조회
@generation_router.get("/generate/{project_name}")
async def get_user_project_imgs(project_name: str):
    username = 'johndoe1'
    port = 'http://0.0.0.0:30008'
    service_directory = f'../data/generation/{username}/{project_name}'
    output_path = os.path.join(service_directory, 'output.jpeg')

    if os.path.exists(output_path):
        return {
            "username": username,
            "project": project_name,
            "complete": True,
            "source": f'{port}/generate/{username}/{project_name}/source',
            "target": f'{port}/generate/{username}/{project_name}/target',
            "output": f'{port}/generate/{username}/{project_name}/output',
        }
    else:
        return {
            "username": username,
            "project": project_name,
            "complete": False,
            "source": None,
            "target": None,
            "output": None
        }

# source 이미지 링크로 보내주기
@generation_router.get("/generate/{username}/{project_name}/source")
async def get_source_image(username: str, project_name: str):
    service_directory = f'../data/generation/{username}/{project_name}'
    source_path = os.path.join(service_directory, 'source.jpeg')

    if os.path.exists(source_path):
        with open(source_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)


# target 이미지 링크로 보내주기
@generation_router.get("/generate/{username}/{project_name}/target")
async def get_target_image(project_name: str):
    username = 'johndoe1'
    service_directory = f'../data/generation/{username}/{project_name}'
    target_path = os.path.join(service_directory, 'target.jpeg')

    if os.path.exists(target_path):
        with open(target_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)

# output 이미지 링크로 보내주기
@generation_router.get("/generate/{username}/{project_name}/output")
async def get_output_image(project_name: str):
    username = 'johndoe1'
    service_directory = f'../data/generation/{username}/{project_name}'
    output_path = os.path.join(service_directory, 'output.jpeg')

    if os.path.exists(output_path):
        with open(output_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)