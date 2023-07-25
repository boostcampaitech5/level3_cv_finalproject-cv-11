
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
    user_id = info['user_id']
    username = info['username']
    project_id = info['project_id']
    project_name = info['project_name']
    password = info['password']

    if project_id is None:
        project_id = crud.get_generation_project_id_by_project_name(db = db, project_name = project_name)

    if username is None:
        username =  crud.get_username_by_user_id(db = db, user_id = user_id)
    
    ## running로 state 변경 후 학습 시작
    state_running = crud.update_state_by_project_id(db, project_type ='generate', project_id = project_id, new_state = 'running')
    if not state_running: # DB state -  running 실패
        crud.update_state_by_project_id(db, project_type ='generate', project_id = project_id, new_state = 'error(db)')
    else: # DB state -  running 성공
        user = crud.get_user_for_login(db, username=username, password=password)
        if not user:
            crud.update_state_by_project_id(db, project_type ='generate', project_id = project_id, new_state = 'error(not user)')
            return {"result": False}
        
        source = f'./datas/{username}/generation/{project_name}/source'
        target = f'./datas/{username}/generation/{project_name}/target'
        output = f'./datas/{username}/generation/{project_name}/result'
        try:
            make_synthesis.make_synthesis(target,source,output)
            crud.update_state_by_project_id(db, project_type ='generate', project_id = project_id, new_state = 'finished')
            return {"result": False}
        except: # 학습 오류
            crud.update_state_by_project_id(db, project_type ='generate', project_id = project_id, new_state = 'error(model)')
            return {"result": False}
    
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