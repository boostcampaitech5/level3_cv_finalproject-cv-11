
from fastapi import Depends, APIRouter
from backend.routers import crud
from backend.routers.database import SessionLocal
from deepfake import make_synthesis
from sqlalchemy.orm import Session
import os

generation_router = APIRouter()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## 별도 py로 분리 필요
@generation_router.post("/generation")
def generation(info: dict, db: Session = Depends(get_db)):
    username = info['username']
    project_name = info['project_name']
    password = info['password']
    
    ## running로 state 변경 후 학습 시작
    state_running = crud.update_generation_state_by_projectname(db, username=username, project_type ='generate', project_name = project_name, new_state = 'running')
    if not state_running: # DB state -  running 실패
        crud.update_generation_state_by_projectname(db, username=username, project_type ='generate', project_name = project_name, new_state = 'error-db')
    else: # DB state -  running 성공
        user = crud.get_user_for_login(db, username=username, password=password)
        if not user:
            crud.update_generation_state_by_projectname(db, username=username, project_type ='generate', project_name = project_name, new_state = 'error-not user')
            return {"result": False}
        
        source = f'/opt/ml/level3_cv_finalproject-cv-11/datas/{username}/generation/{project_name}/source'
        target = f'/opt/ml/level3_cv_finalproject-cv-11/datas/{username}/generation/{project_name}/target'
        output = f'/opt/ml/level3_cv_finalproject-cv-11/datas/{username}/generation/{project_name}/result'
        try:
            make_synthesis.make_synthesis(target,source,output)
            crud.update_generation_state_by_projectname(db, username=username, project_type ='generate', project_name = project_name, new_state = 'finished')
        except: # 학습 오류
            crud.update_generation_state_by_projectname(db, username=username, project_type ='generate', project_name = project_name, new_state = 'error-model')
    
    port = 'http://0.0.0.0:30007'
    result_path = output + '/source.jpeg'

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