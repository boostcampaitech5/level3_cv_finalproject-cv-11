# Getting Started with FastAPI
# python version
python 3.8 (aistage v100 server - python 3.8.5)

## install pyenv
1. `apt-get update`
2. `apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev`
    option select : 6(Asia)  → 69(Seoul) 
3. `curl https://pyenv.run | bash`
4. `vi ~/.bashrc
    edit mode : esc + i
   insert
    ```
    export PATH="${HOME}/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    ```
   exit `:wq`
6. source ~/.bashrc
7. pyenv install {python version} # ex) 3.9.16
8. pyenv versions
9. pyenv shell {python version} # python version activate
   +) pyenv global {python version} # Set the global system Python version

## install poetry
in Linux terminal
1. `curl -sSL https://install.python-poetry.org | python3 -`
2. `vi ~/.bashrc`

    edit mode : esc + i

    insert `export PATH=$PATH:$HOME/.local/bin`

    exit `:wq`
3. `source ~/.bashrc`

## potery start
In the project directory, you can run:


`poetry install`

'poetry shell`

## conda env
0. DB부터 설치할 것
1. conda create -n test python=3.9.7
2. conda activate test
3. pip install -r requirements.txt
    - v100에서 설치가 안된다
    1. conda init bash
    2. source ~/.bashrc
    3. 다시 pip install

## backend start
`python3 main.py`

## install mysql
1.install mysql  
`apt-get install mysql-server mysql-client libmysqlclient-dev`  
2. check installed mysql version  
`mysql --version`

## config mysqy database, table(ver2)
## setting
0. start mysql server  
`service mysql start`
1. make root user & make user_db database  
`mysqladmin -u root create deepfake -p`
2. connect mysql with root user  
`mysql -u root -p`

## make table
3. activate deepfake database  
`use deepfake;`

4. make table  
`CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) UNIQUE NOT NULL,
    signin_name VARCHAR(255)
);`

`CREATE TABLE user_generation (
    user_id INT,
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
`

`CREATE TABLE user_detection (
    user_id INT,
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);`

`CREATE TABLE generation (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(255),
    start_time DATETIME,
    end_time DATETIME,
    state VARCHAR(255)
);
`

`CREATE TABLE detection (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(255),
    start_time DATETIME,
    end_time DATETIME,
    output VARCHAR(255),
    race INT,
    gender INT,
    age INT,
    state VARCHAR(255),
    rating INT
);`

8. change table charset to utf-8
`ALTER TABLE users CONVERT TO CHARSET UTF8;`
`ALTER TABLE user_generation CONVERT TO CHARSET UTF8;`
`ALTER TABLE user_detection CONVERT TO CHARSET UTF8;`
`ALTER TABLE generation CONVERT TO CHARSET UTF8;`
`ALTER TABLE detection CONVERT TO CHARSET UTF8;`


## config mysql database, table(ver1)

0. start mysql server  
`service mysql start`
1. make root user & make user_db database  
`mysqladmin -u root create user_db -p`
2. connect mysql with root user  
`mysql -u root -p`
3. activate user_db database  
`use user_db;`
4. make table  
`create table users (
        username varchar(255) primary key,
        hashed_password varchar(255) not null,
        signin_name varchar(255) not null
        );`
5. insert test user info  
`insert into users values ("temp_username", "temp_hashed_password", "temp_email@temp.com");`
7. check user info  
`select * from users;`
8. change table charset to utf-8
`ALTER TABLE users CONVERT TO CHARSET UTF8;`

user table info may change accoring to development  
when error caused by db remake table by command again


# 스키마와 users 테이블 생성 이후 조회하기

1. 관리자로 mysql 접속
    mysql -u root -p
2. 스키마 조회 및 선택
    SHOW SCHEMAS;
    USE user_db

3. 테이블 조회 및 users 테이블 select
    SHOW TABLES;
    select * from users;


