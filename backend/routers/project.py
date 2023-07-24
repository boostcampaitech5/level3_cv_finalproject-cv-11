import os
from typing import List
from fastapi import File, UploadFile, APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from backend.routers import crud, model, schemas
from backend.routers.database import SessionLocal, engine
from datetime import datetime
# from backend.routers.user import get_db # Dependency

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## DB 세팅
model.Base.metadata.create_all(bind=engine)


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

project_router = APIRouter()

# 프로젝트 리스트 조회
@project_router.get("/{project_type}/{username}")
async def project_list(project_type : str, username:str, db: Session = Depends(get_db)):
    try:
        project_list = crud.get_all_project_by_username(db= db, username= username, project_type = project_type)
        return {'username' : username, 'project_type' : project_type, 'project_len' : len(project_list), 'project_list' : project_list, "message" : '프로젝트 조회 성공'}
    except:
        return {"message": "프로젝트 조회 실패"}

# 신규 프로젝트 생성
@project_router.post("/{project_type}/{username}/start")
async def create_user_project(project_type : str, username: str, db: Session = Depends(get_db)):
    # 특정 유저 폴더 여부 확인
    user_dir = f'./datas/{username}'
    make_folder(user_dir)
    if project_type == 'generate':
        # 특정 유저의 generation 폴더 여부 확인, 없으면 생성
        user_project_dir = os.path.join(user_dir, 'generation')
        make_folder(user_project_dir)

    elif project_type == 'detect':
        # 특정 유저의 generation 폴더 여부 확인, 없으면 생성
        user_project_dir = os.path.join(user_dir, 'detection')
        make_folder(user_project_dir)
    else:
        pass

    # try:
    # 현재 시간 기준으로 project 폴더 생성
    current_time = datetime.now()
    project_name = current_time.strftime("%y%m%d%H%M%S")
    project_dir = os.path.join(user_project_dir, f'{project_name}')
    make_folder(project_dir)
    # except:
    #     return {'result' : False, 'username': username, 'project_type' : project_type, 'project_name': project_name, "message": "Fail - created project folders "}

    # DB 신규 프로젝트 insert
    project_dict = {
        'user_name' : username,
        'project_name' : project_name,
        'state' : 'created',
        'start_time' : current_time
    }
    project = schemas.ProjectCreate(**project_dict)
    result = crud.create_project(db = db, project_type =project_type, project = project) # return T or F

    if result:
        return {'result' : True, 'username': username, 'project_type' : project_type, 'project_name': project_name, "message": "Project Create Success"}
    else:
        # delete_folder(project_dir) # 해당 프로젝트 자체를 삭제함
        return {'result' : False, 'username': username, 'project_type' : project_type, 'project_name': project_name, "message": "Fail - insert project to DB "}

# 생성 프로젝트 이미지 저장 - 1개 이미지만
@project_router.post("/generate/{username}/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_generation_file(username : str, project_name : str, source_file: UploadFile = File(...), target_file: UploadFile = File(...)): #usernames : str):
    # source, target, result 폴더 생성
    project_dir = f'./datas/{username}/generation/{project_name}'
    source_dir = os.path.join(project_dir, 'source')
    target_dir = os.path.join(project_dir, 'target')
    result_dir = os.path.join(project_dir, 'result')
    make_folder(source_dir)
    make_folder(target_dir)
    make_folder(result_dir)

    # source, target 순으로 파일 저장
    source_path = os.path.join(source_dir, 'source.jpeg')
    target_path = os.path.join(target_dir, 'target.jpeg')

    # 파일 저장
    with open(source_path, "wb") as buffer:
        buffer.write(await source_file.read())

    # 파일 저장
    with open(target_path, "wb") as buffer:
        buffer.write(await target_file.read())

    return { 'result': True , "message": f"File uploaded successfully."}

#detection 이미지 저장
@project_router.post("/detect/{username}/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_detection_file(username : str, project_name : str,  real_file: List[UploadFile] = File(...), target_file : UploadFile = File(...) ): 
    # source, target, result 폴더 생성
    project_dir = f'./datas/{username}/detection/{project_name}'
    real_dir = os.path.join(project_dir, 'real')
    fake_dir = os.path.join(project_dir, 'fake')
    target_dir = os.path.join(project_dir, 'target')

    make_folder(real_dir)
    make_folder(fake_dir)
    make_folder(target_dir)

    # source, target 순으로 파일 저장
    target_path = os.path.join(target_dir, 'target.jpeg')

    print(real_file)
    # 파일 저장
    for i in real_file:
        real_path = os.path.join(real_dir, f'real_{i.filename}.jpeg')
        with open(real_path, "wb") as buffer:
            buffer.write(await i.read())
    

    with open(target_path, "wb") as buffer:
        buffer.write(await target_file.read())
    
    return { 'result': True , "message": f"File uploaded successfully."}

# 프로젝트 내 이미지 리스트 조회
@project_router.get("/generate/{username}/{project_name}")
async def get_user_project_imgs(username : str, project_name: str):
    port = 'http://49.50.161.98:30007'
    result_dir = f'./datas/{username}/generation/{project_name}/result'
    jpgs = os.listdir(result_dir)
    result_path = result_dir + '/' +jpgs[0]

    if os.path.exists(result_path):
        return {
            "username": username,
            "project": project_name,
            "complete": True,
            "source": f'{port}/generate/{username}/{project_name}/source',
            "target": f'{port}/generate/{username}/{project_name}/target',
            "output": f'{port}/generate/{username}/{project_name}/result',
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

    
@project_router.get("/detect/{username}/{project_name}")
async def get_user_project_imgs(username : str, project_name: str):
    port = 'http://49.50.161.98:30007'
    result_dir = f'./datas/{username}/detection/{project_name}/target'
    jpgs = os.listdir(result_dir)
    result_path = result_dir + '/' +jpgs[0]

    if os.path.exists(result_path):
        return {
            "username": username,
            "project": project_name,
            "complete": True,
            "target": f'{port}/detect/{username}/{project_name}/target',
        }
    else:
        return {
            "username": username,
            "project": project_name,
            "complete": False,
            "target": None,
        }


# source 이미지 링크로 보내주기
@project_router.get("/generate/{username}/{project_name}/source")
async def get_source_image(username: str, project_name: str):
    source_dir = f'./datas/{username}/generation/{project_name}/source'
    source_path = os.path.join(source_dir, 'source.jpeg')

    if os.path.exists(source_path):
        with open(source_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)

# target 이미지 링크로 보내주기
@project_router.get("/generate/{username}/{project_name}/target")
async def get_target_image(username : str, project_name: str):
    target_dir = f'./datas/{username}/generation/{project_name}/target'
    target_path = os.path.join(target_dir, 'target.jpeg')

    if os.path.exists(target_path):
        with open(target_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)

# output 이미지 링크로 보내주기
@project_router.get("/generate/{username}/{project_name}/result")
async def get_result_image(username:str, project_name: str):
    result_dir = f'./datas/{username}/generation/{project_name}/result'
    jpgs = os.listdir(result_dir)
    result_path = result_dir + '/' +jpgs[0]
    # result_path = os.path.join(result_dir, 'result.jpeg')

    if os.path.exists(result_path):
        with open(result_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)

@project_router.get("/detect/{username}/{project_name}/target")
async def get_target_image(username : str, project_name: str):
    target_dir = f'./datas/{username}/detection/{project_name}/target'
    target_path = os.path.join(target_dir, 'target.jpeg')

    if os.path.exists(target_path):
        with open(target_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)