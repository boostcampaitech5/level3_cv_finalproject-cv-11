# Personalized deepfake detection service
Traditional Deepfake detection focuses on Deepfake detection for an unspecified number of people. <br/>
These are ways to improve the performance of benchmark dataset in Deepfake detection competitions. <br/>
Therefore, these methods do not take into account the actual service situation. <br/>
Accordingly, we propose a model structure that improves the performance of the detection model by few shot learning a small amount of victim pictures. <br/>
Finally, we would like to provide the model-based deepfake detection service 'Fakey' to prevent the abuse of deepfake. <br/>



# Team Members

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/hykhhijk">
            <img src="https://avatars.githubusercontent.com/u/58303938?v=4" alt="김용희 프로필" width=120 height=120 />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/HipJaengYiCat">
          <img src="https://avatars.githubusercontent.com/u/78784633?v=4" alt="박승희 프로필" width=120 height=120 />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/imsmile2000">
          <img src="https://avatars.githubusercontent.com/u/69185594?v=4" alt="이윤표 프로필" width=120 height=120 />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/junha-lee">
          <img src="https://avatars.githubusercontent.com/u/44857783?v=4" alt="이준하 프로필" width=120 height=120 />
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/JaiyoungJoo">
          <img src="https://avatars.githubusercontent.com/u/103994779?v=4" alt="주재영 프로필" width=120 height=120 />
        </a>
      </td>
    </tr>
    <tr>
      <td align="center">
        <a href="https://github.com/hykhhijk">
          김용희
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/HipJaengYiCat">
          박승희
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/imsmile2000">
          이윤표
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/junha-lee">
          이준하
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/JaiyoungJoo">
          주재영
        </a>
      </td>
    </tr>
  </table>
</div>

<br/>
<div id="5"></div>


# Environment  
## Google compute engine  
- region: asia-northeast3-b  
- GPU: Nvidia-T4, num:1  (GPU mem:GDDR6 16GB)  
- CPU: n1-standard-4(vCPU 4개, 15GB 메모리)  
- Boot-disk: Ubuntu20.04LTS 50GB
  
<br>

## Cloud SQL
- database engine: MySQL 8.0.31  
- vCPU:2, 8GB 메모리  
- Disk: SSD 50GB

<br>

# Folder Structure
```bash
├─backend
├─checkpoints
├─datas
├─deepfake
├─docs
├─frontend
├─MobileFaceSwap
└─source
```
<br></br>

# Model architecture
![image](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhxaFFSIeXFIl_4XXkPYa8gsbkBxa67EfkhMdMsPsqP2ZFOZcld5yhSVYQSSPhd2Nf9lPL0zqhpeU4m1CENi4_OtV92xaMBWijyGk6tOSgDEGU13_yoniKBNdqsimljMoWHWpZn7QGS_iCDoszS-LKxyg_ZvLu0vt-17PEkjCdswRn3diurt4MzbjijoUr8/s1610/model_architecture.png)



<br>

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
sudo apt install ubuntu-drivers-common -y  
sudo apt install nvidia-driver-515 -y  
wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux.run
```
if above link expired find appropriate version in this link https://developer.nvidia.com/cuda-toolkit-archive  

  
`sudo sh cuda_11.7.0_515.43.04_linux.run` need to wait long time  
![image](https://github.com/boostcampaitech5/level3_cv_finalproject-cv-11/assets/58303938/06df2ae9-883b-4653-a30d-847de3a6a686)  
*remember checkout Driver!*  

  
5. update .bashrc  
add this to /home/USERNAME/.bashrc  
```
export PATH=/usr/local/cuda-11.7/bin${PATH:+:${PATH}}  
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
8. install requirements without dependencies  
`pip install -r requirements.txt --no-deps`  


## Setting mysql database  
0. start mysql server  
`sudo service mysql start`
1. make root user & make user_db database  
`sudo mysqladmin -u root create user_db -p`
2. import default tables
```
for localhost
sudo mysql -u root -p user_db < {home_path}/level3_cv_finalproject-cv-11/deepfake.sql

for Cloud SQL
sudo mysql -u root -p user_db -h {your cloud sql ip} < {home_path}/level3_cv_finalproject-cv-11/deepfake.sql
```
3. connect mysql with root user  
`sudo mysql -u root -p`
4. change mysql security setting for connection  
`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';`  
`FLUSH PRIVILEGES;`  

5. finally set backend/routers/database.py for your database setting
```
in 5~6 line in backend/routers/database.py
SQLALCHEMY_DATABASE_URL = "mysql://root:1234@localhost:3306/user_db?charset=utf8"        #change user user, password for localhost mysql setting
SQLALCHEMY_DATABASE_URL = "mysql://root:1234@34.64.189.15:3306/user_db?charset=utf8"        #For my cloud SQL server
```


## Download model weights
1. download all model weights by below link  
`https://schackr-my.sharepoint.com/:f:/g/personal/hykhhijk_sch_ac_kr/EjauXOPs4RBKh3S2RsNiK2sBQaIiG8quXpdAjJbTo10ncA?e=hDgffg`  
2. move checkpoints folder to right below outr folder and Meta_train_learning_id_60.pt in to datas  
![image](https://github.com/boostcampaitech5/level3_cv_finalproject-cv-11/assets/58303938/bd27ec79-65eb-468d-a7a0-e8085e18c21d)  
structure have to looks like this
