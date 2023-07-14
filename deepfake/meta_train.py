import os
import datetime
import random

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


input_size = 224
code_size = 100
batch_size = 10
LR = 0.0001
max_epoch = 300

def wandb_config():
    wandb.init(config={'batch_size':batch_size,
                    'learning_rate':LR,
                    'max_epoch':max_epoch},
            project='Segmentation',
            entity='aivengers_seg',
            name=f"Meta_train2_learning_epoch={max_epoch}"
            )

def make_dataset(input_size = 224, real_path= '', fake_path= '', target_path= ''):
    # dataset load
    tf = A.Resize(input_size, input_size)
    train_dataset = datas.Inferset(real_path, fake_path, target_path , tf)
    batch_size = 10
    meta_train_loader = DataLoader(
        dataset=train_dataset, 
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        drop_last=True,
    )
    return meta_train_loader

def calculate_metric(y_true, y_pred):
    y_true = [0 if label[0] >= label[1] else 1 for label in y_true]
    y_pred = [0 if label[0] >= label[1] else 1 for label in y_pred]
    return metrics.f1_score(y_true, y_pred), metrics.accuracy_score(y_true, y_pred)

def validation(iteration, model, data_loader):
    print(f'Start validation #{iteration:2d}')
    with torch.no_grad():
        f1 = []
        accuracy = []
        for step, (r_image, f_image, valid_image, target_image, label) in tqdm(enumerate(data_loader), total=len(data_loader)):
            r_image, f_image, valid_image, target_image, label = r_image.cuda(), f_image.cuda(), valid_image.cuda(), target_image.cuda(), label.cuda()       
            model = model.cuda()
            pred = model(r_image, f_image, valid_image)
            m = nn.Sigmoid()
            f1_score, accuracy_ = calculate_metric(m(pred), label)
            f1.append(f1_score)
            accuracy.append(accuracy_)
            
        f1 = np.array(f1).mean()
        accuracy = np.array(accuracy).mean()
        print(
            f'{datetime.datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")} | '
            f'Valid_acc: {round(accuracy,4)} | '
            f'Valid_F1: {round(f1,4)}'
        )
        valid={
            'Valid_acc' :round(accuracy,4),
            'Valid_F1':round(f1,4)}
        wandb.log(valid, step = iteration)

id_ = [i for i in range(62)]
no_synthesis = [8, 14, 15, 18, 36]
test_id = [1,7,11,17,21,27,31,37,41,47,51,57,61]
train_id = list(set(id_) - set(test_id) - set(no_synthesis))
results = []
labels = []

model = models.FewShotModel2()
model = model.cuda()

iteration = 0

for id_ in train_id:
    print(f'start_id_{id_}')
    optimizer = optim.Adam(params=model.parameters(), lr=0.0001, weight_decay=1e-6)
    real_path= f'/opt/ml/level3_cv_finalproject-cv-11/data/celeb-df/meta_train/real/{id_}'
    fake_path= f'/opt/ml/level3_cv_finalproject-cv-11/data/celeb-df/meta_train/fake/{id_}'
    target_path= f'/opt/ml/level3_cv_finalproject-cv-11/data/celeb-df/target/real/{1}/id{1}_0009.000.png'
    user_name = f'id{id_}'
    meta_train_loader = make_dataset(input_size=input_size, real_path=real_path, fake_path=fake_path, target_path=target_path)
    for epoch in range(max_epoch):
        print(f'start_epoch_{epoch}')
        wandb_config()
        # meta_train_loader = make_dataset(input_size=input_size, real_path=real_path, fake_path=fake_path, target_path=target_path)
        for step, (r_image, f_image, valid_image, target_image, label) in tqdm(enumerate(meta_train_loader), total=len(meta_train_loader)):
            r_image, f_image, valid_image, target_image, label = r_image.cuda(), f_image.cuda(), valid_image.cuda(), target_image.cuda(), label.cuda()
            pred = model(r_image, f_image, valid_image)
            m = nn.Sigmoid()
            criterion = nn.BCELoss()
            loss = criterion(m(pred),label)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
                
        print(
            f'{datetime.datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")} | '
            f'Epoch [{epoch+1}/{max_epoch}], '
            f'Step [{step+1}/{len(meta_train_loader)}], '
            f'Loss: {round(loss.item(),4)}'
        )
        train={'Loss':round(loss.item(),4)}
        wandb.log(train, step = iteration)
        if iteration % 5 == 0:
            validation(iteration, model, meta_train_loader)
        iteration += 1
            

        dest = '/opt/ml/level3_cv_finalproject-cv-11/result/fewshot'
        if not os.path.exists(dest):
            os.makedirs(dest)
        output_path = os.path.join(dest, f"Meta_train_learning_id_{id_}.pt")
        torch.save(model, output_path)
        print('save complite' + output_path)








    
        