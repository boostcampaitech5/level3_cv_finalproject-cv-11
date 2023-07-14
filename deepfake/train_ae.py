import os
import datetime
# torch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
import albumentations as A

# visualization
import wandb
import datas
import models

from importlib import import_module
from tqdm.auto import tqdm

import time
from pytz import timezone

input_size = 1024
code_size = 100
batch_size = 16
LR = 0.00001
seed = 0
max_epoch = 500

def wandb_config():
    wandb.init(config={'batch_size':batch_size,
                    'learning_rate':LR,                 #차차 args.~~로 update할 것
                    'seed':seed,
                    'max_epoch':max_epoch},
            project='Segmentation',
            entity='aivengers_seg',
            name=f"AE_MSE_tf={input_size}_cln=True_e={max_epoch}_sd={seed}_combineloss.pt"
            )

def make_dataset(input_size = 224):
    # dataset load
    tf = A.Resize(input_size, input_size)
    
    train_dataset = dataset_ae.AEDataset(transforms=tf)
    valid_dataset = dataset_ae.AEDataset(transforms=tf)
        

    train_loader = DataLoader(
        dataset=train_dataset, 
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        drop_last=True,
    )
    valid_loader = DataLoader(
        dataset=valid_dataset, 
        batch_size=4,
        shuffle=False,
        num_workers=0,
        drop_last=False
    )

    return [train_loader, valid_loader]

models = models.Autoencoder2(input_size,code_size)
models = models.cuda()

data_loader, valid_loader = make_dataset(input_size)

optimizer = optim.Adam(params=models.parameters(), lr=0.0001, weight_decay=1e-6)


wandb_config()
print('starg_train')

for epoch in range(max_epoch):
    for step, images in tqdm(enumerate(data_loader), total=len(data_loader)):
        input_data = images.cuda()
        target_data = input_data.clone()
        output_data, _ = models(input_data)
        
        mse_loss = getattr(import_module("loss"), 'mse_loss')(output_data, target_data)
        # ssim_loss = getattr(import_module("loss"), 'ssim_loss')(output_data, target_data)
        loss = mse_loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (step + 1) % 20 == 0:
            print(
                f'{datetime.datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")} | '
                f'Epoch [{epoch+1}/{max_epoch}], '
                f'Step [{step+1}/{len(data_loader)}], '
                f'Loss: {round(loss.item(),4)}'
            )
            train={'Loss':round(loss.item(),4)}
            wandb.log(train, step = epoch)
        

    output_path = os.path.join('/home/supergalaxy/junha/input/weights', f"AE_MSE_tf={input_size}_cln=True_e={max_epoch}_sd={seed}_combineloss.pt")
    torch.save(models, output_path)
    