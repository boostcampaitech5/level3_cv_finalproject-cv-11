from typing import List
from fastapi import File, UploadFile, APIRouter
from fastapi.responses import HTMLResponse
import os
file_router = APIRouter()

# 이미지 업로드
@file_router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    for i, file in enumerate(files):
        # 파일을 저장할 경로 설정
        user_name = 'users'
        directory = f"./image/{user_name}"
        save_path = os.path.join(directory, f"{i+1}_{file.filename}")

        # 파일을 저장할 폴더 생성
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            return ('Error: Creating directory. ' +  directory)
    
        
        # 파일 저장
        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())
    
    return {"filenames": [file.filename for file in files], "message": "Files uploaded successfully."}


@file_router.get("/upload")
def main():
    content = """
<form action="/upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# 이미지 다운로드
@file_router.get("/download/{user_name}/{image_num}")
async def download_image(image_id: str):
    # 이미지 파일의 경로
    image_path = f"./image/{user_name}/{image_num}"

    
    
    # 이미지 파일을 다운로드하는 응답 반환
    return FileResponse(image_path, media_type="image/jpeg", filename=image_id + ".jpg")

@file_router.post("/download")
async def upload_files(files: List[UploadFile] = File(...)):
    for i, file in enumerate(files):
        # 파일을 저장할 경로 설정
        user_name = 'users'
        directory = f"./image/{user_name}"
        save_path = os.path.join(directory, f"{i+1}_{file.filename}")

        # 파일을 저장할 폴더 생성
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            return ('Error: Creating directory. ' +  directory)
    
        
        # 파일 저장
        with open(save_path, "wb") as buffer:
            buffer.write(await file.read())
    
    return {"filenames": [file.filename for file in files], "message": "Files uploaded successfully."}


@file_router.get("/download")
def main():
    content = """
<form action="/upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>


<head>
    <title>Image Downloader</title>
</head>
<body>
    <h1>Image Downloader</h1>
    <form action="/upload" enctype="multipart/form-data" method="post">
    <a href="/download/image1">Download Image 1</a>
    <br>
    <a href="/download/image2">Download Image 2</a>
</body>
    """
    return HTMLResponse(content=content)