from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql://root:1234@localhost:3306/user_db?charset=utf8"        #change user root, password 1234 for right setting
SQLALCHEMY_DATABASE_URL = "mysql://root:1234@35.205.29.110:3306/user_db?charset=utf8"        #change user root, password 1234 for right setting


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)     #db session

Base = declarative_base()       #db schema?