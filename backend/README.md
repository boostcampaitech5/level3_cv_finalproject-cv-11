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

    insert 'export PATH=$PATH:$HOME/.local/bin'

    exit `:wq`
3. `source ~/.bashrc`

## potery start
In the project directory, you can run:


`poetry install`

'poetry shell`

## backend start
`python3 main.py'

## install mysql
1.install mysql  
`apt-get install mysql-server mysql-client`  
2. check installed mysql version  
`mysql --version`


## config mysql database, table  
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
        email varchar(255) not null
        );`
5. insert test user info  
`insert into users values ("temp_username", "temp_hashed_password", "temp_email@temp.com");`
6. check user info  
`select * from users;`

user table info may change accoring to development  
when error caused by db remake table by command again

