import os

from fastapi import Depends, APIRouter
from backend.routers import crud
from backend.routers.database import SessionLocal
from deepfake import make_synthesis, inference, gradcam
from sqlalchemy.orm import Session


detection_router = APIRouter()
home_path = os.environ['HOME']
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@detection_router.post("/detection")
def detection(info: dict, db: Session = Depends(get_db)):
    username = info['username']
    project_name = info['project_name']
    password = info['password']

    gender = 'man'
    
    ## running로 state 변경 후 학습 시작
    state_running = crud.update_state_by_projectname(db, username=username, project_type ='detect', project_name = project_name, new_state = 'running')
    if not state_running: # DB state -  running 실패
        crud.update_state_by_projectname(db, username=username, project_type ='detect', project_name = project_name, new_state = 'error(db)')
    else: # DB state -  running 성공
        user = crud.get_user_for_login(db, username=username, password=password)
        if not user:
            crud.update_state_by_projectname(db, username=username, project_type ='detect', project_name = project_name, new_state = 'error(not user)')
            return {"result": False}
    
        try:
            model_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/Meta_train_learning_id_60.pt'
            align_path = f'{home_path}/level3_cv_finalproject-cv-11/deepfake/extract_and_align_faces_image.py'
            real_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/real'
            os.system(f'python {align_path} --load_path {real_path} --save_path {real_path}')
            fake_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/fake'
            target_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/target'
            os.system(f'python {align_path} --load_path {target_path} --save_path {target_path}')
            user_name = f'{username}'
            source = f'{home_path}/level3_cv_finalproject-cv-11/source/{gender}'
            #make_synthesis.make_synthesis(real_path,source,fake_path)
            result = inference.inference(model_path,real_path,fake_path,target_path,user_name)
            user_model = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/model/inference.pt'
            gradcam.gradcam(user_model, real_path, fake_path, target_path)
            crud.update_state_by_projectname(db, username=username, project_type ='detect', project_name = project_name, new_state = 'finished')
            return result
        except:
            crud.update_state_by_projectname(db, username=username, project_type ='detect', project_name = project_name, new_state = 'error(model)')