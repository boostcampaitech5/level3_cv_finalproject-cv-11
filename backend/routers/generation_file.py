from typing import List, Dict
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse, FileResponse
import os
import time
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
    username = 'johndoe_1'
    project_name = time.strftime("%y%m%d%H%M%S", time.localtime())
    user_directory = f'../data/generate/{username}/{project_name}'
    make_folder(user_directory)
    return {'username': username, 'project_name' : project_name, "message": f"start generation."}

# 생성하기 서비스 시간 생성
@generation_router.post("/generate/calcel")
async def create_generation():#usernames : str, project_name : str):
    username = 'johndoe_1'
    project_name = '230712150553'
    user_directory = f'../data/generate/{username}/{project_name}'
    delete_folder(user_directory)
    return {'username': username, 'project_name' : project_name, "message": f"project {project_name} delete."}


# 생성하기 이미지 업로드
@generation_router.post("/generate/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_files(project_name : str, files: List[UploadFile] = File(...)): #usernames : str):
    username = 'johndoe_1'

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
async def generation_project_list():#usernames : str):
    username = 'johndoe_1'
    service_directory = f'../data/generation/{username}'
    project_list = [f for f in os.listdir(service_directory) if os.path.isdir(os.path.join(service_directory, f))]
    return {"username": username, "project_list": project_list}


# 이미지 리스트 조회
@generation_router.get("/generate/{project_name}")
async def get_user_folders(project_name : str):# usernames : str
    username = 'johndoe_1'
    service_directory = f'../data/generation/{username}/{project_name}'
    source_path = os.path.join(service_directory, 'source.jpeg')
    target_path = os.path.join(service_directory, 'target.jpeg')
    output_path = os.path.join(service_directory, 'output.jpeg')
    if os.path.exists(output_path):
        return {
            "username": username,
            "project": project_name,
            "complete": True,
            "source": source_path,
            "target": target_path,
            "output": output_path
        }
    else:
        return {
            "username": username,
            "project": project_name,
            "complete": False,
            "source": source_path,
            "target": target_path,
            "output": output_path
        }