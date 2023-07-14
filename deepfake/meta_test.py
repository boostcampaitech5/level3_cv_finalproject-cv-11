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
            name=f"Meta_test_learning_epoch={max_epoch}"
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

def validation(epoch, model, data_loader):
    print(f'Start validation #{epoch:2d}')
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
        wandb.log(valid, step = epoch)

test_id = [1,7,11,17,21,27,31,37,41,47,51,57,61]
results = []
labels = []

for id_ in test_id:

    real_path= f'/opt/ml/deepfake/data/celeb-df/meta_test/real/{id_}'
    fake_path= f'/opt/ml/deepfake/data/celeb-df/meta_test/fake/{id_}'
    target_path= f'/opt/ml/deepfake/data/celeb-df/target/real/{id_}/id{id_}_0009.000.png'
    user_name = f'id{id_}'

    model = torch.load('/opt/ml/deepfake/result/fewshot/Metalearning_tf=224_cln=True_e=60_sd=0.pt')
    model = model.cuda()

    wandb_config()
    print('start_train')

    optimizer = optim.Adam(params=model.parameters(), lr=0.0001, weight_decay=1e-6)
    meta_train_loader = make_dataset(input_size=input_size, real_path=real_path, fake_path=fake_path, target_path=target_path)
    for epoch in range(max_epoch):
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
        wandb.log(train, step = epoch)
        if epoch % 5 == 0:
            validation(epoch, model, meta_train_loader)
            

    dest = f'/opt/ml/deepfake/result/fewshot/{user_name}'
    if not os.path.exists(dest):
        os.makedirs(dest)
                    
    output_path = os.path.join(dest, f"Meta_test_learning.pt")
    torch.save(model, output_path)
    print('save complite' + output_path)

    print('-'*50)
    print('Inference')
    model = torch.load(output_path)
    #m = nn.Sigmoid()

    print('Inference Fake')
    pngs = os.listdir(f'/opt/ml/deepfake/data/celeb-df/target/fake/{id_}')
    for i in tqdm(pngs):
        target_path= f'/opt/ml/deepfake/data/celeb-df/target/fake/{id_}/{i}'
        target_loader = make_dataset(input_size=input_size, real_path=real_path, fake_path=fake_path, target_path=target_path)
        (_, _, _, target_image, _) = next(iter(target_loader))
        target_image = target_image.cuda()
        for step, (r_image, f_image, valid_image, _, label) in enumerate(meta_train_loader):
            r_image, f_image, valid_image, label = r_image.cuda(), f_image.cuda(), valid_image.cuda(), label.cuda()
            pred = model(r_image, f_image, target_image)
            pred = torch.sum(pred, axis=0)
            
        if pred[0] >= pred[1]:
            results.append(0)
        else:
            results.append(1)
        labels.append(1)

    print('Inference Real')
    pngs = os.listdir(f'/opt/ml/deepfake/data/celeb-df/target/real/{id_}')
    for i in tqdm(pngs):
        target_path= f'/opt/ml/deepfake/data/celeb-df/target/real/{id_}/{i}'
        target_loader = make_dataset(input_size=input_size, real_path=real_path, fake_path=fake_path, target_path=target_path)
        (_, _, _, target_image, _) = next(iter(target_loader))
        target_image = target_image.cuda()
        for step, (r_image, f_image, valid_image, _, label) in enumerate(meta_train_loader):
            r_image, f_image, valid_image, label = r_image.cuda(), f_image.cuda(), valid_image.cuda(), label.cuda()
            pred = model(r_image, f_image, target_image)
            pred = torch.sum(pred, axis=0)
            
        if pred[0] >= pred[1]:
            results.append(0)
        else:
            results.append(1)
        labels.append(0)

print(results)
print(labels)
    
f1, acc = metrics.f1_score(results,labels), metrics.accuracy_score(results,labels)
print(f'acc : {acc}, f1 : {f1}')







    
        