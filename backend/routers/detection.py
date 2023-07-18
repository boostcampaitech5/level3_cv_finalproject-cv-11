
from fastapi import Depends, APIRouter
from backend.routers import crud
from backend.routers.database import SessionLocal
from deepfake import make_synthesis, inference
from sqlalchemy.orm import Session

detection_router = APIRouter()
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
            model_path = '/opt/ml/level3_cv_finalproject-cv-11/datas/Meta_train_learning_id_60.pt'
            real_path = f'/opt/ml/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/real'
            fake_path = f'/opt/ml/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/fake'
            target_path = f'/opt/ml/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/target'
            user_name = f'{username}'
            source = '/opt/ml/level3_cv_finalproject-cv-11/source'
            make_synthesis.make_synthesis(real_path,source,fake_path)
            result = inference.inference(model_path,real_path,fake_path,target_path,user_name)
            crud.update_state_by_projectname(db, username=username, project_type ='detect', project_name = project_name, new_state = 'finished')
            return result
        except:
            crud.update_state_by_projectname(db, username=username, project_type ='detect', project_name = project_name, new_state = 'error(model)')