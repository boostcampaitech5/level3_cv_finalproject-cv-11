import os

from fastapi import Depends, APIRouter
from backend.routers import crud
from backend.routers.database import SessionLocal
from deepfake import make_synthesis, inference, gradcam
from sqlalchemy.orm import Session
import nvidia_smi


detection_router = APIRouter()
home_path = os.environ['HOME']
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_gpu_memory():
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
    mb = 1024*1024
    gpu_memory = info.free/mb
    nvidia_smi.nvmlShutdown()
    return gpu_memory


@detection_router.post("/detection")
def detection(info: dict, db: Session = Depends(get_db)):
    user_id = info['user_id']
    username = info['username']
    project_id = info['project_id']
    project_name = info['project_name']
    password = info['password']

    if project_id is None:
        project_id = crud.get_generation_project_id_by_project_name(db = db, project_name = project_name)

    if username is None:
        username =  crud.get_username_by_user_id(db = db, user_id = user_id)
    
    ## 인물 정보 불러오기
    project_info = crud.get_project_info_by_id(db=db, project_id = project_id, project_type = 'detect') # 인물 정보
    race = project_info.race
    age = project_info.age
    gender = project_info.gender
    gender_path = 'man' if gender == 0 else 'woman' # man -0,  woman - 1#

    #gpu mem, db detection status 체크하여 detection user 2명 유지
    #아래로 이동시킬때 running 1늘려줘야함
    free_gpu = get_gpu_memory()
    detection_running = crud.get_detection_status(db)
    if free_gpu < 5000 or detection_running >=2:
        print(f"free_gpu: {free_gpu}")
        print(f"detection_running: {detection_running}")
        return False

    ## running로 state 변경 후 학습 시작
    state_running = crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'running')
    if not state_running: # DB state -  running 실패
        crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'error(db)')
    else: # DB state -  running 성공
        user = crud.get_user_for_login(db=db, username=username, password=password)
        if not user:
            crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'error(not user)')
            return {"result": False}
    
        try:
            model_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/Meta_train_learning_id_60.pt'
            align_path = f'{home_path}/level3_cv_finalproject-cv-11/deepfake/extract_and_align_faces_image.py'
            data_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}'
            real_path = f'{data_path}/real'
            os.system(f'python {align_path} --load_path {real_path} --save_path {real_path}')
            fake_path = f'{data_path}/fake'
            target_path = f'{data_path}/target'
            os.system(f'python {align_path} --load_path {target_path} --save_path {target_path}')
            source = f'{home_path}/level3_cv_finalproject-cv-11/source/{gender_path}'
            make_synthesis.make_synthesis(real_path,source,fake_path)
            infer_path = f'{home_path}/level3_cv_finalproject-cv-11/deepfake/inference.py'

            ##inference
            os.system(f'python {infer_path} --model_path {model_path} --real_path {real_path} --fake_path {fake_path} --target_path {target_path} --source {source} --username {username} --project_name {project_name} >> {data_path}/result.txt')
            with open(f"{data_path}/result.txt", "r") as ping:
                result = ping.readlines()[-2]
            crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'finished')# 상태 업데이트
            return result
        except:
            crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'error(model)')