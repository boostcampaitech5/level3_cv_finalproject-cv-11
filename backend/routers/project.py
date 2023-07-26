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


# ## DB 세팅
# model.Base.metadata.create_all(bind=engine)


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
@project_router.get("/{project_type}/{user_identifier}")
async def project_list(project_type: str, user_identifier: str, db: Session = Depends(get_db)):
    # username가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier

    try:
        # username을 user_id로 바꾸기 위해, user_id가 없는 경우 username으로부터 user_id를 가져옴
        user_id = int(username) if username.isdigit() else crud.get_user_id_by_username(db, username)
        username = crud.get_username_by_user_id(db, username) if username.isdigit() else username

        if user_id is None:
            return {"message": "사용자를 찾을 수 없습니다."}

        project_list = crud.get_all_project_info_by_id(db=db, user_id=user_id, project_type=project_type)
        return {'user_id': user_id, 'project_type': project_type, 'project_len': len(project_list),
                'project_list': project_list, "message": '프로젝트 조회 성공'}
    except:
        return {"message": "프로젝트 조회 실패"}

# 신규 프로젝트 생성
# create_project_info 함수
def insert_project_id(user_identifier: str, project_type: str, db: Session):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier


    if user_id is None:
        return None, None, None, None, None

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

    # 현재 시간과 현재 시간으로 프로젝트 네임 생성
    current_time = datetime.now()
    project_name = current_time.strftime("%y%m%d%H%M%S")

    # 프로젝트 네임으로 폴더 생성
    project_dir = os.path.join(user_project_dir, f'{project_name}')
    make_folder(project_dir)

    # 프로젝트 네임으로 프로젝트 id 생성
    user_project_dict = {
        'user_id': user_id,
        'project_name': project_name,
    }
    user_project = schemas.ProjectIdCreate(**user_project_dict)
    project_id = crud.create_project_id(db=db, project_type=project_type, user_project=user_project)

    return project_type, project_id, project_name, current_time

# project 정보를 insert하는 함수
def insert_project_info(project_type : str, project_id: int, project_name: str, current_time: datetime, db: Session):
    if project_type == 'generate':
        generation_project = model.GenerationProject(
            project_id=project_id,
            project_name=project_name,
            start_time=current_time,
            end_time=None,  # 이 값은 나중에 설정해야 함
            state='created'
        )
        db.add(generation_project)
        db.commit()
        db.refresh(generation_project)


    elif project_type == 'detect':
        detection_project = model.DetectionProject(
            project_id=project_id,
            project_name=project_name,
            start_time=current_time,
            end_time=None,  # 이 값은 나중에 설정해야 함
            output='',  # 이 값은 나중에 설정해야 함
            race=0,  # 이 값은 나중에 설정해야 함
            gender=0,  # 이 값은 나중에 설정해야 함
            age=0,  # 이 값은 나중에 설정해야 함
            state='created',
            rating=0  # 이 값은 나중에 설정해야 함
        )
        db.add(detection_project)
        db.commit()
        db.refresh(detection_project)
    else:
        pass

# 프로젝트 생성 API 수정
@project_router.post("/{project_type}/{user_identifier}/start")
async def create_user_project(project_type: str, user_identifier: str, db: Session = Depends(get_db)):
    # try:

    # project 정보를 생성
    project_type, project_id, project_name, current_time = insert_project_id(user_identifier, project_type, db)
    
    if project_id is None:
        return {"message": "사용자를 찾을 수 없습니다."}

    # project 정보를 insert
    insert_project_info(project_type, project_id, project_name, current_time, db)

    return {'result': True, 'username': user_identifier, 'project_type': project_type,
            'project_id' : project_id, 'project_name': project_name, "message": "Project Create Success"}
    # except:
    #     return {"message": "Fail - insert project to DB"}


# 생성 프로젝트 이미지 저장 - 1개 이미지만
@project_router.post("/generate/{user_identifier}/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_generation_file(user_identifier : str, project_name : str, source_file: UploadFile = File(...), target_file: UploadFile = File(...), db: Session = Depends(get_db)): #usernames : str):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier

    
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
@project_router.post("/detect/{user_identifier}/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_detection_file(user_identifier : str, project_name : str,  real_file: List[UploadFile] = File(...), target_file : UploadFile = File(...), db: Session = Depends(get_db)): 
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier

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
@project_router.get("/generate/{user_identifier}/{project_name}")
async def get_user_project_imgs(user_identifier : str, project_name: str, db: Session = Depends(get_db)):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier

    port = 'http://115.85.182.51:30007'
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

    
@project_router.get("/detect/{user_identifier}/{project_name}")
async def get_user_project_imgs(user_identifier : str, project_name: str, db: Session = Depends(get_db)):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier

    port = 'http://115.85.182.51:30007'
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
@project_router.get("/generate/{user_identifier}/{project_name}/source")
async def get_source_image(user_identifier: str, project_name: str, db: Session = Depends(get_db)):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier


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
@project_router.get("/generate/{user_identifier}/{project_name}/target")
async def get_target_image(user_identifier : str, project_name: str, db: Session = Depends(get_db)):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier


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
@project_router.get("/generate/{user_identifier}/{project_name}/result")
async def get_result_image(user_identifier:str, project_name: str, db: Session = Depends(get_db)):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier

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

@project_router.get("/detect/{user_identifier}/{project_name}/target")
async def get_target_image(user_identifier : str, project_name: str, db: Session = Depends(get_db)):
    # user_identifier가 int이면 user_id로 쓰고 str이면 user_id를 불러옴
    user_id = int(user_identifier) if user_identifier.isdigit() else crud.get_user_id_by_username(db, user_identifier)
    username = crud.get_username_by_user_id(db, user_identifier) if user_identifier.isdigit() else user_identifier

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