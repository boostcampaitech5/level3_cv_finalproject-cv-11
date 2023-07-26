
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import os
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import cv2
from torchvision import transforms

plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap

home_path = os.environ['HOME']


save_feat=[]
def normalize(tensor):
    x = tensor - tensor.min()
    x = x / (x.max() + 1e-9)
    return x

# Dataset
class MaskDataset(Dataset):
  def __init__(self, data_roots, input_size=224, transform=None):
    super(MaskDataset, self).__init__()
    real_root = data_roots[0]
    fake_root = data_roots[1]
    target_root = data_roots[2]

    self.rfilename = os.listdir(real_root)[0]
    self.rimg_list = os.path.join(real_root, self.rfilename)
    self.ffilename = os.listdir(fake_root)[0]
    self.fimg_list = os.path.join(fake_root, self.ffilename)
    self.tfilename = os.listdir(target_root)[0]
    self.timg_list = os.path.join(target_root, self.tfilename)

    self.len = len(self.rimg_list)
    self.input_size = input_size
    self.transform = transform

  def __getitem__(self, index):
    rimg_path = self.rimg_list
  
    # Image Loading
    rimg = cv2.imread(rimg_path)
    rimg = cv2.cvtColor(rimg, cv2.COLOR_BGR2RGB)
    rimg = rimg/255.

    if self.transform:
      rimg = self.transform(rimg)

    fimg_path = self.fimg_list
  
    # Image Loading
    fimg = cv2.imread(fimg_path)
    fimg = cv2.cvtColor(fimg, cv2.COLOR_BGR2RGB)
    fimg = fimg/255.

    if self.transform:
      fimg = self.transform(fimg)

    timg_path = self.timg_list
  
    # Image Loading
    timg = cv2.imread(timg_path)
    timg = cv2.cvtColor(timg, cv2.COLOR_BGR2RGB)
    timg = timg/255.

    if self.transform:
      timg = self.transform(timg)

    return rimg, fimg, timg

  def __len__(self):
    return self.len


def image_tensor_to_numpy(tensor_image):
    # If this is already a numpy image, just return it
    if type(tensor_image) == np.ndarray:
        return tensor_image
    
    # Make sure this is a tensor and not a variable
    if type(tensor_image) == Variable:
        tensor_image = tensor_image.data
    
    # Convert to numpy and move to CPU if necessary
    np_img = tensor_image.detach().cpu().numpy()
    
    # If there is no batch dimension, add one
    if len(np_img.shape) == 3:
        np_img = np_img[np.newaxis, ...]
    
    # Convert from BxCxHxW (PyTorch convention) to BxHxWxC (OpenCV/numpy convention)
    np_img = np_img.transpose(0, 2, 3, 1)
    
    return np_img

def image_numpy_to_tensor(np_image):
    if len(np_image.shape) == 3:
        np_image = np_image[np.newaxis, ...]
    
    # Convert from BxHxWxC (OpenCV/numpy) to BxCxHxW (PyTorch)
    np_image = np_image.transpose(0, 3, 1, 2)
    
    tensor_image = torch.from_numpy(np_image).float()
    
    return tensor_image

def hook_feat(module, input, output):
    save_feat.append(output)
    return output


save_grad=[]
def hook_grad(grad):
    save_grad.append(grad)
    return grad



def vis_gradcam(model, real, false, target):

    model.eval()
    # (1) Reister hook for storing layer activation of the target layer (bn5_2 in backbone)
    # model.backbone.bn5_2.register_forward_hook(hook_feat)
    model.backbone.sm_image_embedder.efficient_net._conv_stem.register_forward_hook(hook_feat)

    # (2) Forward pass to hook features
    real, false, target = real.unsqueeze(0), false.unsqueeze(0), target.unsqueeze(0)
    s_ = model(real,false,target)
    s = s_[0]
    # (3) Register hook for storing gradients
    save_feat[0].register_hook(hook_grad)
    # (4) Backward score
    y = torch.argmax(s).item()
    s_y = s[y]
    s_y.backward()
    # Compute activation at global-average-pooling layer
    gap_layer  = torch.nn.AdaptiveAvgPool2d(1)
    alpha = gap_layer(save_grad[0][0].squeeze())
    A = save_feat[0].squeeze()
    # (1) Compute grad_CAM 
    # (You may need to use .squeeze() to feed weighted_sum into into relu_layer)
    relu_layer = torch.nn.ReLU()
    weighted_sum = torch.sum(alpha*A, dim=0)
    grad_CAM = relu_layer(weighted_sum)
    grad_CAM = grad_CAM.unsqueeze(0)
    grad_CAM = grad_CAM.unsqueeze(0)
    # (2) Upscale grad_CAM
    # (You may use defined upscale_layer)
    upscale_layer = torch.nn.Upsample(scale_factor=target.shape[-1]/grad_CAM.shape[-1], mode='bilinear')
    grad_CAM = upscale_layer(grad_CAM)
    grad_CAM = grad_CAM/torch.max(grad_CAM)
    grad_CAM = grad_CAM.cpu()

    img_np = image_tensor_to_numpy(target)
    if len(img_np.shape) > 3:
        img_np = img_np[0]
    img_np = normalize(img_np)

    grad_CAM = grad_CAM.squeeze().detach().numpy()

    

    plt.figure(figsize=(8, 8))
    plt.imshow(img_np)
    plt.imshow(grad_CAM, cmap='jet', alpha = 0.5)
    plt.savefig(f'{target_path}/grad.png')

    return grad_CAM

def gradcam(model_path, real_path, fake_path, target_path):
    model = torch.load(model_path).double()
    input_size = 224
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((224,224)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                            std=[0.229, 0.224, 0.225])
    ])

    paths = [real_path,fake_path, target_path]

    data = MaskDataset(paths, input_size=input_size, transform=transform)

    real_img, fake_img, target_img = next(iter(data))

    grad_CAM = vis_gradcam(model, real_img.cuda(), real_img.cuda(), real_img.cuda())


if __name__ == '__main__':
    model_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/id/model/inference.pt'
    real_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/id/detection/230725033532/real'
    fake_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/id/detection/230725033532/fake'
    target_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/id/detection/230725033532/target'
    gradcam(model_path, real_path, fake_path, target_path)