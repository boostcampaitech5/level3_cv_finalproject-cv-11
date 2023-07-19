# Getting Started with Google Cloud Platform

## Make GCP instance 
0. [Make gcp instance](https://console.cloud.google.com/compute/instances)
1. call for GPU allocation [참고]: https://kim6394.tistory.com/98  

2. GCP config
```
region: asia-northeast3-b  
GPU: Nvidia-T4, num:1  
CPU: n1-standard-4(vCPU 4개, 15GB 메모리)
Boot-disk: Ubuntu20.04LTS at least 30GB
Firewall: allow all
```
3. make SSH-key & add metadata & access with VSCode to GCE  
follow this link to make key by puttygen(don't need private key)https://amanokaze.github.io/blog/Connect-GCE-using-VS-Code/

4. install cuda
```  
sudo apt install ubuntu-drivers-common  
sudo apt install nvidia-driver-515  
wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux.run
```
if above link expired find appropriate version in this link https://developer.nvidia.com/cuda-toolkit-archive  

  
`sudo sh cuda_11.7.0_515.43.04_linux.run` need to wait long time  
![image](https://github.com/boostcampaitech5/level3_cv_finalproject-cv-11/assets/58303938/06df2ae9-883b-4653-a30d-847de3a6a686)  
*remember checkout Driver!*  

  
5. update .bashrc  
add this to /home/USERNAME/.bashrc  
```
export PATH=/usr/local/cuda-11.7/bin${PATH:+:${PATH}}`  
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
```

6. run bashrc  
`source ~/.bashrc`  
7. check installed CUDA  
`nvcc --version`
8. download cudnn fron oneDrive  
filename is cudnn-linux-x86_64-8.5.0.96_cuda11-archive.tar.zip
9. install cudnn  
`tar -xvf cudnn-linux-x86_64-8.5.0.96_cuda11-archive.tar.xz`
```
sudo cp cudnn-linux-x86_64-8.5.0.96_cuda11-archive/include/cudnn*.h /usr/local/cuda/include
sudo cp -P cudnn-linux-x86_64-8.5.0.96_cuda11-archive/lib/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```
10. check installed cudnn  
`cat /usr/local/cuda/include/cudnn_version.h | grep CUDNN_MAJOR -A 2`
11. reboot to apply changes  
`sudo reboot`


## Make conda virtualenv  
1. download conda  
`wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh`  
2. install conda  
`bash Anaconda3-2020.07-Linux-x86_64.sh`  
![image](https://github.com/boostcampaitech5/level3_cv_finalproject-cv-11/assets/58303938/af29ce0c-c5ed-4947-8116-eb96cc26dc4d)  
check "yes" at here  
3. run bashrc  
`source ~/.bashrc`  
4. make virtual env  
`conda create -n final python=3.9.7`  
`conda activate final`  
5. install mysql  
`sudo apt-get install mysql-server mysql-client libmysqlclient-dev`  
6. clone our github and cd move to it  
`git clone https://github.com/boostcampaitech5/level3_cv_finalproject-cv-11.git`  
after this move to develop branch and pull  
8. install requirements  
`pip install -r requirements.txt`  


## Setting mysql database  
0. start mysql server  
`sudo service mysql start`
1. make root user & make user_db database  
`sudo mysqladmin -u root create user_db -p`
2. connect mysql with root user  
`sudo mysql -u root -p`
3. activate user_db database  
`use user_db;`
4. make table  
```
create table users (
        username varchar(255) primary key,
        hashed_password varchar(255) not null,
        signin_name varchar(255) not null
        );
```
5. insert test user info  
`insert into users values ("temp_username", "temp_hashed_password", "temp_email@temp.com");`
7. check user info  
`select * from users;`
8. change table charset to utf-8  
`ALTER TABLE users CONVERT TO CHARSET UTF8;`  
9. change mysql security setting for connection  
`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';`
