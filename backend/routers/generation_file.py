from typing import List, Dict
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse
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



# 생성하기 이미지 업로드
@generation_router.post("/generation-source-upload") # 생성하기-대상이미지업로드버튼
async def upload_files(files: List[UploadFile] = File(...)): # user_info - dict으로된 정보
    user_info = fake_users_db["johndoe"]
    # 파일 수 확인 
    if len(files) > 1:
        return ('대상 이미지는 한 장만 넣어주세요')
    
    # 유저 폴더 생성
    # user_directory = f'../data/generation/{user_info['username']}_{user_info['user_id']}' # ex) johndoe_1
    user_directory = f'../data/generation/johndoe_1' # ex) johndoe_1
    make_folder(user_directory)

    # 서비스요청시간별 폴더 생성
    current_time = time.strftime("%y%m%d%H%M%S", time.localtime()) # 현재 시간 
    service_directory = os.path.join(user_directory, current_time) # ex) ./username_user_id/230711134530
    service_directory = os.path.join(service_directory, 'real') # ex) ./username_user_id/230711134530
    make_folder(service_directory)

    for i, file in enumerate(files):
        # 파일명 생성
        save_path = os.path.join(service_directory, f"{i+1}_{file.filename}") # f"{file.filename}" 택1

        # 파일 저장
        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())
    
    return {"filenames": [file.filename for file in files], "message": f"File uploaded successfully."}


# 이미지 다운로드
@generation_router.get("/generation-download")
async def download_image(service_time: str):
    user_info = fake_users_db["johndoe"]
    service_time = '230712010930'
    # 이미지 파일의 경로
    # image_path = f"../data/generation/{user_info['username']}_{user_info['user_id']}/{service_time}/output.jpeg"
    image_path = f"../data/generation/johndoe_1/{service_time}/output.jpeg"

    # 이미지 파일을 다운로드하는 응답 반환
    return FileResponse(image_path, media_type="image/jpeg", filename="output.jpg")

## html 
@generation_router.get("/generation-source-upload")
def main():
    content = """
<form action="/generation-source-upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@generation_router.get("/generation-download")
def main():
    content = """
<head>
    <title>Image Downloader</title>
</head>
<body>
    <h1>Image Downloader</h1>
    <form action="/generation-download" enctype="multipart/form-data" method="post">
    <a href="/download/image1">Download Image 1</a>
    <br>
    <a href="/download/image2">Download Image 2</a>
    </form>
</body>
    """
    return HTMLResponse(content=content)
