import os

home_path = os.environ['HOME']

pyfile = f'{home_path}/level3_cv_finalproject-cv-11/MobileFaceSwap/image_test.py'


def make_synthesis(target_img_path, source_img_path, output_dir):
    target_imgs = os.listdir(target_img_path)
    source_imgs = os.listdir(source_img_path)
    for target_img_, source_img_ in zip(target_imgs,source_imgs):
        target_img = os.path.join(target_img_path,target_img_)
        source_img = os.path.join(source_img_path,source_img_)
        os.system(f'python {pyfile} --target_img_path {source_img} --source_img_path {target_img} --output_dir {output_dir}')
        print(f'complete_{target_img_}')

    dir = f'{home_path}/level3_cv_finalproject-cv-11/MobileFaceSwap/temp'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

if __name__ == '__main__':
    username = 'yoon'
    project_name = '230717175420'
    source_img_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/generation/{project_name}/source'
    target_img_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/generation/{project_name}/target'
    output_dir = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/generation/{project_name}/result'
    make_synthesis(target_img_path, source_img_path, output_dir)