import os
import warnings
warnings.filterwarnings('ignore')

pyfile = '/opt/ml/level3_cv_finalproject-cv-11/MobileFaceSwap/image_test.py'
source_img_path = f'/opt/ml/level3_cv_finalproject-cv-11/data/original'



def make_synthesis(target_img_path,output_dir):
    target_imgs = os.listdir(target_img_path)[:30]
    source_imgs = os.listdir(source_img_path)[:30]
    for target_img_, source_img_ in zip(target_imgs,source_imgs[:len(target_imgs)]):
        target_img = os.path.join(target_img_path,target_img_)
        source_img = os.path.join(source_img_path,source_img_)
        os.system(f'python {pyfile} --target_img_path {source_img} --source_img_path {target_img} --output_dir {output_dir}')
    print(f'complete_{target_img_}')

target_img_paths = os.listdir('/opt/ml/level3_cv_finalproject-cv-11/data/celeb-df/meta_test/real')

for i in target_img_paths:
    target_img_path = f'/opt/ml/level3_cv_finalproject-cv-11/data/celeb-df/meta_test/real/{i}'
    output_dir = f'/opt/ml/level3_cv_finalproject-cv-11/data/celeb-df/meta_test/mobilefaceswap/{i}'
    make_synthesis(target_img_path,output_dir)
