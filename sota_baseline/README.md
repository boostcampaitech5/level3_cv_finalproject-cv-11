# Combining EfficientNet and Vision Transformers for Video Deepfake Detection
[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/combining-efficientnet-and-vision/deepfake-detection-on-dfdc)](https://paperswithcode.com/sota/deepfake-detection-on-dfdc?p=combining-efficientnet-and-vision)

현재 개발 중인 모델과 비교하기 위한 대조군으로 DFDC State of the Art 모델을 사용[<a href="https://arxiv.org/abs/2107.02612">Pre-print PDF</a> | <a href="https://www.springerprofessional.de/en/combining-efficientnet-and-vision-transformers-for-video-deepfak/20403304">Springer</a>]

## 모델 특징
Combining EfficientNet and Vision Transformers

## 설치
repository 복사 및 이동
```
git clone https://github.com/boostcampaitech5/level3_cv_finalproject-cv-11.git

cd level3_cv_finalproject-cv-11/sota_baseline/cross-efficient-vit
```
conda 가상환경 설치
```
conda env create --file environment.yml
conda activate deepfakes
export PYTHONPATH=.
```
## 전처리
- videos를 face crop image로 생성하는 과정이 필요
- MTCNN을 이용하여 face detection 후 json 파일 생성
```
cd preprocessing
python3 detect_faces.py --data_path "path/to/videos"
```
- json 파일을 이용해 face crop 후 저장
```
python3 extract_crops.py --data_path "path/to/videos" --output_path "path/to/output"
```

## test용 dataset
- DFDC : 
    - https://www.kaggle.com/competitions/deepfake-detection-challenge/data
    - https://ai.facebook.com/datasets/dfdc/
- celeb-df : 
    - https://github.com/yuezunli/celeb-deepfakeforensics

## test 결과
- kaggle train dataset
    - DFDC pre-trained 
    - train dataset 400개 video를 이용
    - 총 400개의 video 중 382개의 video만 face detection
    - Test Accuracy : 0.9685863874345549 
    - Loss : 0.41152558 
    - F1 : 0.9801324503311258

<img src="https://github.com/JaiyoungJoo/product_serving_practice/assets/103994779/81352fd1-e045-49a1-a7b0-873043276ac7"  width="70%" height="70%">

<img src="https://github.com/JaiyoungJoo/product_serving_practice/assets/103994779/cdc1c369-0231-4700-ae97-30d610b10bd4"  width="70%" height="70%">

- celeb-df videos dataset
    - DFDC pre-trained
    - celeb-df video 중 real video 590개, fake video 590개 이용
    - 총 400개의 video 중 382개의 video만 face detection
    - Test Accuracy : 0.8466101694915255 
    - Loss : 0.6256666 
    - F1 : 0.8617265087853323

<img src="https://github.com/JaiyoungJoo/product_serving_practice/assets/103994779/67e4caad-057d-4ad1-a580-c50024eba9ac"  width="70%" height="70%">

<img src="https://github.com/JaiyoungJoo/product_serving_practice/assets/103994779/3244a56f-4629-4b5a-b03a-6f34f2528ddd"  width="70%" height="70%">

- celeb-df image dataset
    - DFDC pre-trained
    - celeb-df video를 face crop한 image로 성능평가
    - real image 38120개 중 random 1000장 추출
    - fake image 357211개 중 random 1000장 추출
    - sigmoid threshold를 0.5으로 할 경우
        - Accuracy : 0.7795
    - sigmoid threshold를 0.6으로 할 경우
        - Accuracy : 0.7805
