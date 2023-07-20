'''
CREATE TABLE generation (
  project_id INT AUTO_INCREMENT PRIMARY KEY,
  project_name VARCHAR(255),
  user_id INT
  user_name VARCHAR(255),
  start_time DATETIME,
  end_time DATETIME,
  state VARCHAR(255),
);

INSERT INTO generation (project_name, user_name, start_time, end_time, state, output_url)
VALUES ('230101000000', 'test', '2023-01-01 00:00:00', NULL, 'running', NULL);


CREATE TABLE detection (
  project_id INT AUTO_INCREMENT PRIMARY KEY,
  project_name VARCHAR(255),
  user_id INT
  user_name VARCHAR(255),
  start_time DATETIME,
  end_time DATETIME,
  state VARCHAR(255),
  output VARCHAR(255)
);

INSERT INTO detection (project_name, user_name, start_time, end_time, state, output_url)
VALUES ('230101000000', 'test', '2023-01-01 00:00:00', NULL, 'running', NULL);
'''



from sqlalchemy.orm import Session

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import mysql.connector

# MySQL 서버에 연결
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)

# 커서 생성
cursor = conn.cursor()

# SELECT 쿼리 실행
select_query = "SELECT * FROM your_table"
cursor.execute(select_query)
result = cursor.fetchall()

for row in result:
    print(row)

# INSERT 쿼리 실행
insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
data = ("value1", "value2")
cursor.execute(insert_query, data)
conn.commit()

# 연결 종료
cursor.close()
conn.close()


import pandas as pd
import os
import pymysql
from sqlalchemy import create_engine
import datetime
import re
import datetime

# DB업로드
def db_connection(host_name='ds'):
    host_url = "db.ds.mycelebs.com"
    user_nm = "root"
    passwd = "1234"
    port_num = 3306
    db_name = "maimovie_kr"
    conn = pymysql.connect(host=host_url, user=user_nm, passwd=passwd, port = port_num, charset='utf8', cursorclass=pymysql.cursors.DictCursor) # cursorclass=pymysql.cursors.DictCursor 추가     # db=db,
    return conn
#engine_upload (jangho)
def engine_upload(upload_df: object, host_name: object = 'ds', db_name: object = 'maimovie_kr', table_name: object = 'ranking') -> object:
    host_url = "db.ds.mycelebs.com"
    user_nm = "shee3475"
    passwd = "welcome2019!"
    port_num = 3306
    db_name = "maimovie_kr"
    engine = create_engine(f'mysql+pymysql://{user_nm}:{passwd}@{host_url}:{port_num}/{db_name}?charset=utf8mb4')
    engine_conn = engine.connect()
    upload_df.to_sql(table_name, engine_conn, if_exists='append', index=None)
    engine_conn.close()
    engine.dispose()
    
### title 전처리 함수
def award_title(df):
    if "(" in df:
        items = re.findall('\(([^)]+)', df)
        items = items[0]
        return items
    else:
        return df
    
def award_title_2(df):
    if "(" in df:
        df = df+")"
        return df
    else:
        return df
    
    # DB : naver_award
conn = db_connection('mai')
maimovie_kr_naver_award = pd.read_sql(f"SELECT * FROM maimovie_kr.maimovie_kr_naver_award", conn)
#maimovie_kr_naver_award_cnt = pd.read_sql(f"SELECT COUNT(*) FROM maimovie_kr.maimovie_kr_naver_award", conn)
conn.close()