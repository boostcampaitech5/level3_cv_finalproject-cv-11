from sqlalchemy.orm import Session
# import model, schemas
from backend.routers import model, schemas

from passlib.context import CryptContext

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


def create_user(db: Session, user: schemas.UserCreate):         
    hashed_password = get_password_hash(user.password)        #암호화 알고리즘 추가
    # user = get_user_by_username(username=user.username, db=db)       #id겹치면 return None
    # if not user:
        # return None
    db_user = model.User(username=user.username,signin_name=user.signin_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

## project - generation / detection
def create_project(db: Session, project_type: str, project: schemas.ProjectCreate):
    if project_type == 'generation':
        project_data = model.GenerationProject(
            username=project.username,
            project_name=project.project_name,
            state=project.state, # created, running, finish, error
            start_time=project.start_time
        )
    elif project_type == 'detection':
        project_data = model.DetectionProject(
            username=project.username,
            project_name=project.project_name,
            state=project.state,
            start_time=project.start_time
        )
    else:
        return False

    try:
        db.add(project_data)
        db.commit()
        db.refresh(project_data)
        return True
    except:
        return False


def get_all_project_by_username(db: Session, username: str, project_type :str):
    if project_type == 'generation':
        return db.query(model.GenerateProject).filter(model.GenerateProject.user_name == username)
    else:
        return db.query(model.DetectionProject).filter(model.DetectionProject.user_name == username)

def get_project_by_username(db: Session, username: str, project_name : str, project_type :str):
    if project_type == 'generation':
        return db.query(model.GenerateProject).filter(model.GenerateProject.user_name == username).filter(model.GenerateProject.project_name == project_name).first()
    else:
        return db.query(model.DetectionProject).filter(model.DetectionProject.user_name == username).filter(model.DetectionProject.project_name == project_name).first()
