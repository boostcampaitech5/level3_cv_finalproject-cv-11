from typing import List, Dict
from fastapi import File, UploadFile, APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, Response
import os
from datetime import datetime

# 폴더 생성
def make_folder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        return ('Error: Creating directory. ' +  path)

# # # 폴더 삭제
# # def delete_folder(path):
# #     try:
# #         if not os.path.exists(path):
# #             os.remove(path)
# #     except OSError:
# #         return ('Error: not exists directory. ' +  path)

generation_router = APIRouter()

# generation 프로젝트 리스트 조회
@generation_router.get("/generate/{username}")
async def generation_project_list(username:str):
    user_dir = f'./datas/{username}'
    if not os.path.exists(user_dir):
        return {"username": username, "project_len" : 0, "message" : '생성된 유저 폴더가 없습니다'}
    
    user_generation_dir = os.path.join(user_dir, 'generation')
    if not os.path.exists(user_generation_dir):
            return {"username": username, "project_len" : 0, "message" : '생성된 generate 프로젝트가 없습니다'}

    project_list = os.listdir(user_generation_dir)
    return {"username": username, "project_len" : len(project_list), "project_list": project_list}

# 생성 - 신규 프로젝트 생성
@generation_router.post("/generate/{username}/start")
async def create_generation(username: str):
    # 특정 유저 폴더 여부 확인
    user_dir = f'./datas/{username}'
    make_folder(user_dir)

    # 특정 유저의 generation 폴더 여부 확인, 없으면 생성
    user_generation_dir = os.path.join(user_dir, 'generation')
    make_folder(user_generation_dir)

    # 현재 시간 기준으로 project 폴더 생성
    project_name = datetime.now().strftime("%y%m%d%H%M%S")
    project_dir = os.path.join(user_generation_dir, f'{project_name}')
    make_folder(project_dir)

    return {'username': username, 'project_name': project_name, "message": "Project Create Success"}

# 생성 - 신규 프로젝트 생성
@generation_router.post("/detect/{username}/start")
async def create_detection(username: str):
    # 특정 유저 폴더 여부 확인
    user_dir = f'./datas/{username}'
    make_folder(user_dir)

    # 특정 유저의 generation 폴더 여부 확인, 없으면 생성
    user_generation_dir = os.path.join(user_dir, 'detection')
    make_folder(user_generation_dir)

    # 현재 시간 기준으로 project 폴더 생성
    project_name = datetime.now().strftime("%y%m%d%H%M%S")
    project_dir = os.path.join(user_generation_dir, f'{project_name}')
    make_folder(project_dir)

    return {'username': username, 'project_name': project_name, "message": "Project Create Success"}



# 생성 - 프로젝트 이미지 업로드
@generation_router.post("/generate/{username}/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_generate_file(username : str, project_name : str, source_file: UploadFile = File(...), target_file: UploadFile = File(...)): #usernames : str):
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
@generation_router.post("/detect/{username}/{project_name}/upload") # 생성하기-대상이미지업로드버튼
async def upload_detect_file(username : str, project_name : str,  real_file: List[UploadFile] = File(...), target_file : UploadFile = File(...) ): #usernames : str):
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


    # 파일 저장
    for i in real_file:
        real_path = os.path.join(real_dir, f'real_{i.filename}.jpeg')
        with open(real_path, "wb") as buffer:
            buffer.write(await i.read())
    

    with open(target_path, "wb") as buffer:
        buffer.write(await target_file.read())
    
    return { 'result': True , "message": f"File uploaded successfully."}


# 프로젝트 내 이미지 리스트 조회
@generation_router.get("/generate/{username}/{project_name}")
async def get_user_project_imgs(username : str, project_name: str):
    port = 'http://118.67.133.181:30007'
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

# source 이미지 링크로 보내주기
@generation_router.get("/generate/{username}/{project_name}/source")
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
@generation_router.get("/generate/{username}/{project_name}/target")
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
@generation_router.get("/generate/{username}/{project_name}/result")
async def get_result_image(username:str, project_name: str):
    result_dir = f'./datas/{username}/generation/{project_name}/result'
    result_path = os.path.join(result_dir, 'source.jpeg')

    if os.path.exists(result_path):
        with open(result_path, "rb") as file:
            contents = file.read()
        response = Response(content=contents, media_type="image/jpeg")
        response.headers["Content-Disposition"] = "inline"
        return response
    else:
        return Response(status_code=404)


# # 생성 - 프로젝트 이미지 업로드 - 파일 여러개 버전
# @generation_router.post("/generate/{username}/{project_name}/upload") # 생성하기-대상이미지업로드버튼
# async def upload_files(username : str, project_name : str, source_files: List[UploadFile] = File(...), target_files: List[UploadFile] = File(...)): #usernames : str):
#     # # 파일 수 확인 
#     # if len(files) != 2:
#     #     return { 'result': False , "message": f"정확히 각각의 1개 이미지를 업로드해주세요."}

#     # source, target, result 폴더 생성
#     project_dir = f'./datas/{username}/generation/{project_name}'
#     source_dir = os.path.join(project_dir, 'source')
#     target_dir = os.path.join(project_dir, 'target')
#     result_dir = os.path.join(project_dir, 'result')
#     make_folder(source_dir)
#     make_folder(target_dir)
#     make_folder(result_dir)

#     # source, target 순으로 파일 저장
#     source_path = os.path.join(source_dir, 'source.jpeg')
#     target_path = os.path.join(target_dir, 'target.jpeg')

#     # 파일 저장
#     with open(source_path, "wb") as buffer:
#         buffer.write(await source_files[0].read())

#     # 파일 저장
#     with open(target_path, "wb") as buffer:
#         buffer.write(await target_files[0].read())
    
#     return { 'result': True , "message": f"File uploaded successfully."}
