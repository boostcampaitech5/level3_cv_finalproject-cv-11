import random
import numpy as np
import os
import cv2
import torch
from torch.utils.data import Dataset

O_IMAGE_ROOT = "/opt/ml/deepfake/data/original"
M_IMAGE_ROOT = "/opt/ml/deepfake/data/FaceShifter"

R_IMAGE_ROOT = "/opt/ml/deepfake/celeb-df/image/real"
S_IMAGE_ROOT = "/opt/ml/deepfake/celeb-df/image/synthesis"

no_synthesis = [8, 14, 15, 18, 36]
min_synthesis = 834
id_ = [i for i in range(62)]
test_id = [1,7,11,17,21,27,31,37,41,47,51,57,61]
train_id = list(set(id_) - set(test_id) - set(no_synthesis))
target_video_id = [3,7,8]
train_video_id = [0,1,2,4,5,6]

class AEDataset(Dataset):
    def __init__(self, transforms=None, image_root=O_IMAGE_ROOT, person = 0, test= False):
        if not person:
            jpgs = os.listdir(image_root)
            _filenames = np.array(jpgs)
        elif test:
            image_root = image_root + f'/{person}'
            jpgs = os.listdir(image_root)
            _filenames = np.array(jpgs[:-2])
        else:
            image_root = image_root + f'/{person}'
            jpgs = os.listdir(image_root)
            _filenames = np.array(jpgs[-2:])

        self.image_root = image_root
        self.filenames = _filenames
        self.transforms = transforms
    
    def __len__(self):
        return len(self.filenames)
    
    def __getitem__(self, item):
        image_name = self.filenames[item]
        image_path = os.path.join(self.image_root, image_name)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image / 255.
        
        if self.transforms is not None:
            inputs = {"image": image}
            result = self.transforms(**inputs)
            image = result["image"]

        # to tenser will be done later
        image = image.transpose(2, 0, 1)    # make channel first
        
        image = torch.from_numpy(image).float()
            
        return image

'''
real_pngs = os.listdir(R_IMAGE_ROOT)
fake_pngs = os.listdir(S_IMAGE_ROOT)

train_fakes = [i for i in fake_pngs if int(i.split('_')[1][2:]) in train_id]
test_fakes = [i for i in fake_pngs if int(i.split('_')[1][2:]) in test_id]

train_reals = [i for i in real_pngs if int(i.split('_')[0][2:]) in train_id]
test_reals = [i for i in real_pngs if int(i.split('_')[0][2:]) in test_id]
'''


class MetaTrainset(Dataset):
    def __init__(self, transforms=None, id_ = 0):
        train_real = [i for i in train_reals if int(i.split('_')[0][2:]) == id_ and int(i.split('_')[1][3]) in train_video_id]
        train_fake = [i for i in train_fakes if int(i.split('_')[1][2:]) == id_ and int(i.split('_')[2][3]) in train_video_id]
        target_real = [i for i in train_reals if int(i.split('_')[0][2:]) == id_ and int(i.split('_')[1][3]) in target_video_id]
        target_fake = [i for i in train_fakes if int(i.split('_')[1][2:]) == id_ and int(i.split('_')[2][3]) in target_video_id]
        self.transforms = transforms
        self.r_filenames = random.sample(train_real, 50)
        self.f_filenames = random.sample(train_fake, 50)
        self.r_target_filenames = random.sample(target_real, 50)
        self.f_target_filenames = random.sample(target_fake, 50)

    def __len__(self):
        return len(self.r_filenames)

    def __getitem__(self, item):
        r_image_name = self.r_filenames[item]
        r_image_path = os.path.join(R_IMAGE_ROOT, r_image_name)

        f_image_name = self.f_filenames[item]
        f_image_path = os.path.join(S_IMAGE_ROOT, f_image_name)

        r_target_image_name = self.r_target_filenames[item]
        r_target_image_path = os.path.join(R_IMAGE_ROOT, r_target_image_name)

        f_target_image_name = self.f_target_filenames[item]
        f_target_image_path = os.path.join(S_IMAGE_ROOT, f_target_image_name)
        
        
        r_image = cv2.imread(r_image_path)
        r_image = r_image / 255.
        
        f_image = cv2.imread(f_image_path)
        f_image = f_image / 255.

        if item%2 == 0:
            target_image = cv2.imread(r_target_image_path)
            label = np.array([1,0])
        elif item%2 != 0:
            target_image = cv2.imread(f_target_image_path)
            label = np.array([0,1])

        target_image = target_image / 255.


        if self.transforms is not None:
            inputs = {"image": r_image}
            result = self.transforms(**inputs)
            r_image = result["image"]

            inputs = {"image": f_image}
            result = self.transforms(**inputs)
            f_image = result["image"]

            inputs = {"image": target_image}
            result = self.transforms(**inputs)
            target_image = result["image"]


        # to tenser will be done later
        r_image = r_image.transpose(2, 0, 1)
        f_image = f_image.transpose(2, 0, 1)
        target_image = target_image.transpose(2, 0, 1)
        
        r_image = torch.from_numpy(r_image).float()
        f_image = torch.from_numpy(f_image).float()
        target_image = torch.from_numpy(target_image).float()
        label = torch.from_numpy(label).float()
            
        return r_image, f_image, target_image, label
        
    
    
class MetaInferset(Dataset):
    def __init__(self, transforms=None, id_ = 0):
        infer_real = [i for i in test_reals if int(i.split('_')[0][2:]) == id_ and int(i.split('_')[1][3]) == 9]
        infer_fake = [i for i in test_fakes if int(i.split('_')[1][2:]) == id_ and int(i.split('_')[2][3]) == 9]
        self.transforms = transforms

        self.r_infer_filenames = random.sample(infer_real,1)
        self.f_infer_filenames = random.sample(infer_fake,)
        

    def __len__(self):
        return len(self.r_filenames)

    def __getitem__(self, item):
        
        r_infer_image_name = self.r_infer_filenames[item]
        r_infer_image_path = os.path.join(R_IMAGE_ROOT, r_infer_image_name)

        f_infer_image_name = self.f_infer_filenames[item]
        f_infer_image_path = os.path.join(S_IMAGE_ROOT, f_infer_image_name)
        
        
        

        if item%2 == 0:
            infer_image = cv2.imread(r_infer_image_path)
            infer_label = np.array([1,0])
            
        elif item%2 != 0:
            infer_image = cv2.imread(f_infer_image_path)
            infer_label = np.array([0,1])
            

        infer_image = infer_image / 255.
        

        if self.transforms is not None:
            
            inputs = {"image": infer_image}
            result = self.transforms(**inputs)
            infer_image = result["image"]


        # to tenser will be done later
        infer_image = infer_image.transpose(2, 0, 1)
        
        infer_image = torch.from_numpy(infer_image).float()
        infer_label = torch.from_numpy(infer_label).float()
            
        return infer_image, infer_label
    




class Inferset(Dataset):
    def __init__(self, real_path, fake_path, target_path, transforms = None):

        self.real_path = real_path
        self.fake_path = fake_path
        self.target_path = target_path

        real = random.sample(os.listdir(real_path), 15)
        fake = random.sample(os.listdir(fake_path), 15)
        target = os.listdir(target_path)
        
        self.real_pngs = real[:10]
        self.fake_pngs = fake[:10]
        self.valid_pngs = real[10:] + fake[10:]
        self.target_png = target[0]
        
        self.transforms = transforms
        
        
    def __len__(self):
        return len(self.real_pngs)
    
    def __getitem__(self, item):
        
        r_infer_image_name = self.real_pngs[item]
        r_infer_image_path = os.path.join(self.real_path, r_infer_image_name)

        f_infer_image_name = self.fake_pngs[item]
        f_infer_image_path = os.path.join(self.fake_path, f_infer_image_name)

        valid_image_name = self.valid_pngs[item]

        if item<5: 
            valid_image_path = os.path.join(self.real_path, valid_image_name)
            label = np.array([1,0])
        else:
            valid_image_path = os.path.join(self.fake_path, valid_image_name)
            label = np.array([0,1])

        target_image_path = os.path.join(self.target_path, self.target_png)
        print(target_image_path)
        
        
        r_infer_image = cv2.imread(r_infer_image_path)
            
        f_infer_image = cv2.imread(f_infer_image_path)

        valid_image = cv2.imread(valid_image_path)

        target_image = cv2.imread(target_image_path)
            

        r_infer_image = r_infer_image / 255.
        f_infer_image = f_infer_image / 255.
        valid_image = valid_image / 255.
        target_image = target_image / 255.
        

        if self.transforms is not None:
            
            inputs = {"image": r_infer_image}
            result = self.transforms(**inputs)
            r_infer_image = result["image"]
            
            inputs = {"image": f_infer_image}
            result = self.transforms(**inputs)
            f_infer_image = result["image"]

            inputs = {"image": valid_image}
            result = self.transforms(**inputs)
            valid_image = result["image"]

            inputs = {"image": target_image}
            result = self.transforms(**inputs)
            target_image = result["image"]


        # to tenser will be done later
        r_infer_image = r_infer_image.transpose(2, 0, 1)
        f_infer_image = f_infer_image.transpose(2, 0, 1)
        valid_image = valid_image.transpose(2, 0, 1)
        target_image = target_image.transpose(2, 0, 1)
        
        r_infer_image = torch.from_numpy(r_infer_image).float()
        f_infer_image = torch.from_numpy(f_infer_image).float()
        valid_image = torch.from_numpy(valid_image).float()
        target_image = torch.from_numpy(target_image).float()
        label = torch.from_numpy(label).float()
            
        return r_infer_image, f_infer_image, valid_image, target_image, label
        
        
        




    

