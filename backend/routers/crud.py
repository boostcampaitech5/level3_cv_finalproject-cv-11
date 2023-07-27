from sqlalchemy.orm import Session
# import model, schemas
from backend.routers import model, schemas
from passlib.context import CryptContext
import datetime

SECRET_KEY = "88c2a56e0d8fc664a5d89fc7a9ade75b118beb5beacd317e54d4841b4926570e"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_id(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()

# 사용자 이름(username)으로부터 사용자 ID(user_id)를 가져오는 함수
def get_user_id_by_username(db: Session, username: str):
    user = db.query(model.User).filter(model.User.username == username).first()
    if user:
        return user.user_id
    else:
        return None
    
# 사용자 ID(user_id) 으로부터 사용자 이름(username)를 가져오는 함수
def get_username_by_user_id(db: Session, user_id: str):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if user:
        return user.username
    else:
        return None
    
def get_user_for_login(db: Session, username: str, password):
    user = db.query(model.User).filter(model.User.username == username).first()
    if not user:
        return None
    validation = verify_password(password, user.hashed_password)
    if validation==True:
        return user
    else:
        return None

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

# 프로젝트 명칭(project_name)으로부터 프로젝트 id(project_id)를 가져오는 함수
def get_generation_project_id_by_project_name(db: Session, project_name: str):
    project = db.query(model.UsersGeneration).filter(model.UsersGeneration.project_name == project_name).first()
    if project:
        return project.project_id
    else:
        return None
    
def get_detection_project_id_by_project_name(db: Session, project_name: str):
    project = db.query(model.UsersDetection).filter(model.UsersDetection.project_name == project_name).first()
    if project:
        return project.project_id
    else:
        return None
    

def create_user(db: Session, user: schemas.UserCreate):         
    hashed_password = get_password_hash(user.password)        #암호화 알고리즘 추가
    db_user = model.User(username=user.username,signin_name=user.signin_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

## project id 생성
def create_project_id(db: Session, project_type: str, user_project: schemas.ProjectIdCreate):
    if project_type == 'generate':
        user_project_data = model.UsersGeneration(
            user_id=user_project.user_id,
            project_id = None,
            project_name=user_project.project_name,
        )
    elif project_type == 'detect':
        user_project_data = model.UsersDetection(
            user_id      = user_project.user_id,
            project_id = None,
            project_name = user_project.project_name,
        )
    else:
        pass

    db.add(user_project_data)
    db.commit()
    db.refresh(user_project_data)
    return user_project_data.project_id

## project id와 project info를 받아 생성
def create_project(db: Session, project_type: str, project_id : int, project: schemas.ProjectCreate):
    if project_type == 'generate':
        project_data = model.GenerationProject(
            project_id   = project_id,
            project_name = project.project_name,
            state        = project.state, # created, running, finish, error
            start_time   = project.start_time
        )
    elif project_type == 'detect':
        project_data = model.DetectionProject(
            project_id   = project_id,
            project_name = project.project_name,
            state        = project.state, # created, running, finish, error
            start_time   = project.start_time
        )
    else:
        pass

    db.add(project_data)
    db.commit()
    db.refresh(project_data)
    return True
    # except:
    #     return False

## user_id로 목록 조회
def get_all_project_id_by_id(db: Session, user_id: int, project_type :str):
    if project_type == 'generate':
        return db.query(model.UsersGeneration).filter(model.UsersGeneration.user_id == user_id).all()
    else:
        return db.query(model.UsersDetection).filter(model.UsersDetection.user_id == user_id).all()

## all_project_id로 프로젝트 정보 조회
def get_all_project_info_by_id(db: Session, user_id: int, project_type: str):
    project_info_list = []
    project_ids = [project.project_id for project in get_all_project_id_by_id(db, user_id, project_type)]

    if project_type == 'generate':
        projects = db.query(model.GenerationProject).filter(model.GenerationProject.project_id.in_(project_ids)).all()
    else:
        projects = db.query(model.DetectionProject).filter(model.DetectionProject.project_id.in_(project_ids)).all()

    for project in projects:
        project_info = {
            'project_id': project.project_id,
            'project_name': project.project_name,
            'start_time': project.start_time,
            'end_time': project.end_time,
            'state': project.state,
        }
        if project_type == 'detect':
            project_info.update({
                'output': project.output,
                'race': project.race,
                'gender': project.gender,
                'age': project.age,
                'rating': project.rating,
            })
        project_info_list.append(project_info)

    return project_info_list

# project_id로 project_info 조회
def get_project_info_by_id(db: Session, project_id: int, project_type: str):
    if project_type == 'generate':
        return db.query(model.GenerationProject).filter(model.GenerationProject.project_id == project_id).first()
    else:
        return db.query(model.DetectionProject).filter(model.DetectionProject.project_id == project_id).first()


## username으로 목록 조회
def get_all_project_by_username(db: Session, username: str, project_type :str):
    if project_type == 'generate':
        return db.query(model.GenerationProject).filter(model.GenerationProject.username == username).all()
    else:
        return db.query(model.DetectionProject).filter(model.DetectionProject.username == username).all()

def get_project_by_username(db: Session, username: str, project_name : str, project_type :str):
    if project_type == 'generate':
        return db.query(model.GenerationProject).filter(model.GenerationProject.username == username).filter(model.GenerateProject.project_name == project_name).first()
    else:
        return db.query(model.DetectionProject).filter(model.DetectionProject.username == username).filter(model.DetectionProject.project_name == project_name).first()


def get_detection_status(db: Session):
    return len(db.query(model.DetectionProject).filter(model.DetectionProject.state == "running").all())


def update_state_by_project_id(db: Session, project_type: str, project_id: int, new_state: str):
    if project_type == 'generate':
        project = db.query(model.GenerationProject).filter_by(project_id=project_id).first()
        if project:
            project.state = new_state
            project.end_time = datetime.datetime.now()
            db.commit()
            db.refresh(project)
            return True
        return False
    elif project_type == 'detect':
        project = db.query(model.DetectionProject).filter_by(project_id=project_id).first()
        if project:
            project.state = new_state
            project.end_time = datetime.datetime.now()
            db.commit()
            db.refresh(project)
            return True
        return False
    else:
        return False

def update_detect_person_by_project_id(db: Session, project_id: int, age : str, gender : str, race : str):
    project = db.query(model.DetectionProject).filter_by(project_id=project_id).first()
    if project:
        project.race = race
        project.gender = gender
        project.age = age
        db.commit()
        db.refresh(project)
        return True
    return False

def update_detect_output_by_project_id(db: Session, project_id: int, output: str):
    project = db.query(model.DetectionProject).filter_by(project_id=project_id).first()
    if project:
        project.output = output
        db.commit()
        db.refresh(project)
        return True
    return False

def update_detect_rating_by_project_id(db: Session, project_id: int, rating: str):
    project = db.query(model.DetectionProject).filter_by(project_id=project_id).first()
    if project:
        project.rating = rating
        db.commit()
        db.refresh(project)
        return True
    return False


# def update_state_by_projectname(db: Session, username: str, project_type: str, project_name: str, new_state: str):
#     if project_type == 'generate':
#         project = db.query(model.GenerationProject).filter_by(username=username, project_name=project_name).first()
#         if project:
#             project.state = new_state
#             project.end_time = datetime.datetime.now()
#             db.commit()
#             db.refresh(project)
#             return True
#         return False
#     elif project_type == 'detect':
#         project = db.query(model.DetectionProject).filter_by(username=username, project_name=project_name).first()
#         if project:
#             project.state = new_state
#             project.end_time = datetime.datetime.now()
#             db.commit()
#             db.refresh(project)
#             return True
#         return False
#     else:
#         return False


