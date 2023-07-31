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
#from deepfake import datas
import datas
from tqdm.auto import tqdm
from pytz import timezone
import gradcam
import argparse
import mysql.connector



db_config = {
    'host': '34.64.189.15',
    'user': 'root',
    'password': '1234',
    'database': 'user_db',
}



def parse_args():
    parser = argparse.ArgumentParser()
    home_path = os.environ['HOME']
    username = 'id'
    project_name = '230725033532'
    model_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/Meta_train_learning_id_60.pt'
    real_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/real'
    fake_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/fake'
    target_path = f'{home_path}/level3_cv_finalproject-cv-11/datas/{username}/detection/{project_name}/target'
    source = f'{home_path}/level3_cv_finalproject-cv-11/datas/source/man'
    
    parser.add_argument('--model_path', type=str, default=model_path)
    parser.add_argument('--real_path', type=str, default=real_path)
    parser.add_argument('--fake_path', type=str, default=fake_path)
    parser.add_argument('--target_path', type=str, default=target_path)
    parser.add_argument('--source', type=str, default=source) #얼굴 주변에 마진 추가
    parser.add_argument('--username', type=str, default=username)
    parser.add_argument('--project_name', type=str, default=project_name)

    args = parser.parse_args()
    
    return args

home_path = os.environ['HOME']

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


def main(model_path, real_path, fake_path, target_path, user_name, project_name):
    print(project_name)
    real_path= real_path
    fake_path= fake_path
    target_path= target_path
    user_name = user_name
    input_size = 224
    max_epoch = 1

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
            criterion = nn.MSELoss()
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
            

    dest = f'{home_path}/level3_cv_finalproject-cv-11/datas/{user_name}/model'
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
    print('start grad')
    target_image = target_image[0]
    gradcam.vis_gradcam(model, target_image, target_image, target_image, target_path)
    print('end grad')
    m = nn.Sigmoid()
    pred = torch.sum(m(pred), axis=0)
    if pred[0] >= pred[1]:
        result = 'real'
    else:
        result = 'fake'
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Define the values for the new column and the corresponding project_id to update
        # project_name  # Replace this with the appropriate project_id you want to update
        new_column_value = result  # Replace this with the data you want to add to the new column

        # Define the UPDATE query to add data to the new column
        update_query = "UPDATE detection SET output = %s WHERE project_name = %s"

        # Execute the UPDATE query with the new column value and project_id
        cursor.execute(update_query, (new_column_value, project_name))

        # Commit the changes
        connection.commit()

        print("Data added to the new column successfully!")

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()



    print(result)
    return result
    
    
if __name__ == '__main__':
    args = parse_args()
    result = main(args.model_path, args.real_path, args.fake_path, args.target_path, args.username, args.project_name)