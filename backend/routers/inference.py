
from fastapi import Depends, APIRouter
from deepfake import make_synthesis, inference
from sqlalchemy.orm import Session

from backend.routers import crud
from backend.routers.generation_file import get_user_project_imgs
from backend.routers.user import get_db

inference_router = APIRouter()

# backend > inference.py로 이동
@inference_router.post("/generation")
def generation(info: dict, db: Session = Depends(get_db)):
    username = info['username']
    project_name = info['project_name']
    password = info['password']
    
    user = crud.get_user_for_login(db, username=username, password=password)
    if not user:
        return {"result": False}
    
    source = f'./datas/{username}/generation/{project_name}/source'
    target = f'./datas/{username}/generation/{project_name}/target'
    output = f'./datas/{username}/generation/{project_name}/result'
    make_synthesis.make_synthesis(target,source,output)
    
    return get_user_project_imgs(username, project_name)
    # port = 'http://118.67.133.181:30007'
    # result_path = output + '/source.jpeg'

    # if os.path.exists(result_path):
    #     return {
    #         "username": username,
    #         "project": project_name,
    #         "complete": True,
    #         "source": f'{port}/generate/{username}/{project_name}/source',
    #         "target": f'{port}/generate/{username}/{project_name}/target',
    #         "output": f'{port}/generate/{username}/{project_name}/result',
    #     }
    # else:
    #     return {
    #         "username": username,
    #         "project": project_name,
    #         "complete": False,
    #         "source": None,
    #         "target": None,
    #         "output": None
    #     }
    
@inference_router.post("/detection")
def detection(info: dict, db: Session = Depends(get_db)):
    username = info['username']
    project_name = info['project_name']
    password = info['password']
    
    user = crud.get_user_for_login(db, username=username, password=password)
    if not user:
        return {"result": False}
    
    model_path = './datas/Meta_train_learning_id_60.pt'
    real_path = f'./datas/{username}/detection/{project_name}/real'
    fake_path = f'./datas/{username}/detection/{project_name}/fake'
    target_path = f'./datas/{username}/detection/{project_name}/target'
    user_name = f'{username}'
    source = './source'
    make_synthesis.make_synthesis(real_path,source,fake_path)
    result = inference.inference(model_path,real_path,fake_path,target_path,user_name)
    
    return result

