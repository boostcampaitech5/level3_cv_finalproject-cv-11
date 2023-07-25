
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
    user_id = info['user_id']
    username = info['username']
    project_id = info['project_id']
    project_name = info['project_name']
    password = info['password']
    # race = info['race']
    # gender = info['gender']
    # age = info['age']

    if project_id is None:
        project_id = crud.get_generation_project_id_by_project_name(db = db, project_name = project_name)

    if username is None:
        username =  crud.get_username_by_user_id(db = db, user_id = user_id)
    
    ## running로 state 변경 후 학습 시작
    # person_update = crud.update_detect_person_by_project_id(db=db, project_id = project_id, race = race, gender = gender, age = age) # 인물 정보 업데이트
    person_update = True
    state_running = crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'running')
    if not (state_running and person_update): # DB state -  running 실패
        crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'error(db)')
    else: # DB state -  running 성공
        user = crud.get_user_for_login(db=db, username=username, password=password)
        if not user:
            crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'error(not user)')
            return {"result": False}
    
        try:
            model_path = './datas/Meta_train_learning_id_60.pt'
            real_path = f'./datas/{username}/detection/{project_name}/real'
            fake_path = f'./datas/{username}/detection/{project_name}/fake'
            target_path = f'./datas/{username}/detection/{project_name}/target'
            source = './source'
            make_synthesis.make_synthesis(real_path,source,fake_path)
            result = inference.inference(model_path,real_path,fake_path,target_path,username)
            crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'finished')# 상태 업데이트
            crud.update_detect_output_by_project_id(db=db, project_id =project_id, output = result) # 결과 업데이트 
            
            return result
        except:
            crud.update_state_by_project_id(db=db, project_type ='detect', project_id = project_id, new_state = 'error(model)')