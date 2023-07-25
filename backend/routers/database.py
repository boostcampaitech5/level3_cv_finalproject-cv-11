from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:1234@localhost:3306/deepfake?charset=utf8"        #change user root, password 1234 for right setting

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     #db session

Base = declarative_base()       #db schema?

# 데이터베이스에 테이블이 존재하는지 확인
inspector = inspect(engine)
existing_tables = inspector.get_table_names()