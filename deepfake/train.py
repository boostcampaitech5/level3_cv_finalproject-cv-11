import os
import datetime
# torch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Subset
import albumentations as A
from sklearn import metrics
import numpy as np

# visualization
import wandb
import datas
import models

from importlib import import_module
from tqdm.auto import tqdm

import time
from pytz import timezone

no_synthesis = [8, 14, 15, 18, 36]
min_synthesis = 834
id_ = [i for i in range(62)]
test_id = [1,7,11,17,21,27,31,37,41,47,51,57,61]
train_id = list(set(id_) - set(test_id) - set(no_synthesis))
train_video_id = [0,1,2,4,5,6]
target_video_id = [3,7,8]


input_size = 224
code_size = 100
batch_size = 10
LR = 0.0001
seed = 0
max_epoch = 50

def wandb_config():
    wandb.init(config={'batch_size':batch_size,
                    'learning_rate':LR,             
                    'seed':seed,
                    'max_epoch':max_epoch},
            project='Segmentation',
            entity='aivengers_seg',
            name=f"meta_train_learning_tf={input_size}_cln=True_e={max_epoch}"
            )

def make_dataset(input_size = 224, id_ = 0, few_shot = False):
    # dataset load
    tf = A.Resize(input_size, input_size)
    
    if not few_shot:
        train_dataset = datas.MetaTrainset(transforms=tf, id_ = id_)
        meta_train_loader = DataLoader(
            dataset=train_dataset, 
            batch_size=batch_size,
            shuffle=True,
            num_workers=4,
            drop_last=True,
        )
        return meta_train_loader
    else:
        test_dataset = datas.MetaTestset(transforms=tf, id_ = id_)
        meta_test_loader = DataLoader(
            dataset=test_dataset, 
            batch_size=10,
            shuffle=True,
            num_workers=0,
            drop_last=False
        )
        return meta_test_loader

model = models.FewShotModel2()
model = model.cuda()

wandb_config()
print('start_train')

def calculate_metric(y_true, y_pred):
    y_true = [0 if label[0] >= label[1] else 1 for label in y_true]
    y_pred = [0 if label[0] >= label[1] else 1 for label in y_pred]
    return metrics.f1_score(y_true, y_pred), metrics.accuracy_score(y_true, y_pred)

def validation(epoch, model, data_loader):
    print(f'Start validation #{epoch:2d}')
    with torch.no_grad():
        n_class = 2
        total_loss = 0
        cnt = 0
        f1 = []
        accuracy = []
        for step, (r_image, f_image, target_image, label) in tqdm(enumerate(data_loader), total=len(data_loader)):
            r_image, f_image, target_image, label = r_image.cuda(), f_image.cuda(), target_image.cuda(), label.cuda()       
            model = model.cuda()
            pred = model(r_image, f_image, target_image)
            m = nn.Sigmoid()
            f1_score, accuracy_ = calculate_metric(m(pred), label)
            f1.append(f1_score)
            accuracy.append(accuracy_)
            
        f1 = np.array(f1).mean()
        accuracy = np.array(accuracy).mean()
        print(
            f'{datetime.datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")} | '
            f'Valid_acc: {round(accuracy,4)}'
            f'Valid_F1: {round(f1,4)}'
        )
        valid={
            'Valid_acc' :round(accuracy,4),
            'Valid_F1':round(f1,4)}
        wandb.log(valid, step = epoch)

total_epoch = 0
for e_n, episode in enumerate(train_id):
    print(f'episode #{episode}')
    optimizer = optim.Adam(params=model.parameters(), lr=0.0001, weight_decay=1e-6)
    meta_train_loader = make_dataset(input_size,episode)
    for epoch in range(max_epoch):
        if (epoch+1) % 10 == 0:
            meta_train_loader = make_dataset(input_size,episode)
        for step, (r_image, f_image, target_image, label) in tqdm(enumerate(meta_train_loader), total=len(meta_train_loader)):
            r_image, f_image, target_image, label = r_image.cuda(), f_image.cuda(), target_image.cuda(), label.cuda()
            pred = model(r_image, f_image, target_image)
            m = nn.Sigmoid()
            criterion = nn.BCELoss()
            loss = criterion(m(pred),label)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        total_epoch +=1
            

        print(
            f'{datetime.datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")} | '
            f'Epoch [{epoch+1}/{max_epoch}], '
            f'Episode [{e_n+1}/{len(train_id)}]'
            f'Step [{step+1}/{len(meta_train_loader)}], '
            f'Loss: {round(loss.item(),4)}'
        )
        train={'Loss':round(loss.item(),4)}
        wandb.log(train, step = total_epoch)
        if total_epoch % 5 == 0:
            validation(total_epoch, model, meta_train_loader)
        
                
    
    output_path = os.path.join('/opt/ml/deepfake/result/fewshot', f"Meta_train_learning_tf={input_size}_cln=True_e={episode}.pt")
    torch.save(model, output_path)
    print('save complite' + output_path)
        