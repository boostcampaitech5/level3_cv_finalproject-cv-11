import os
import datetime
# torch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import albumentations as A
from sklearn import metrics
import numpy as np
import datas
from tqdm.auto import tqdm
from pytz import timezone

def make_dataset(input_size = 224, real_path= '', fake_path= '', target_path= ''):
    # dataset load
    tf = A.Resize(input_size, input_size)
    train_dataset = datas.Inferset(real_path, fake_path,target_path , tf)
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
    print(y_true)
    print(y_pred)
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
            f'Valid_acc: {round(accuracy,4)}'
            f'Valid_F1: {round(f1,4)}'
        )


def inference(model_path, real_path, fake_path, target_path, user_name):

    real_path= real_path
    fake_path= fake_path
    target_path= target_path
    user_name = user_name
    input_size = 224
    max_epoch = 30

    model = torch.load(model_path)
    model = model.cuda()

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
        if epoch % 5 == 0:
            validation(epoch, model, meta_train_loader)
            

    dest = f'/opt/ml/level3_cv_finalproject-cv-11/data/{user_name}/model'
    if not os.path.exists(dest):
        os.makedirs(dest)
                    
    output_path = os.path.join(dest, f"inference.pt")
    torch.save(model, output_path)
    print('save complete' + output_path)

    print('Inference')
    model = torch.load(output_path)

    for step, (r_image, f_image, valid_image, target_image, label) in tqdm(enumerate(meta_train_loader), total=len(meta_train_loader)):
        r_image, f_image, valid_image, target_image, label = r_image.cuda(), f_image.cuda(), valid_image.cuda(), target_image.cuda(), label.cuda()
        pred = model(r_image, f_image, target_image)
        pred = torch.sum(pred, axis=0)
        
        if pred[0] >= pred[1]:
            result = 'real'
        else:
            result = 'fake'
        print(result)
        return result





    
if __name__ == '__main__':
    model_path = '/opt/ml/level3_cv_finalproject-cv-11/result/fewshot/foundation_model.pt'
    real_path = '/opt/ml/level3_cv_finalproject-cv-11/data/username/detection/1/real'
    fake_path = '/opt/ml/level3_cv_finalproject-cv-11/data/username/detection/1/fake'
    target_path = '/opt/ml/level3_cv_finalproject-cv-11/data/username/detection/1/target'
    user_name = 'username'
    source = '/opt/ml/level3_cv_finalproject-cv-11/data/source'
    result = inference(model_path,real_path,fake_path,target_path,user_name)