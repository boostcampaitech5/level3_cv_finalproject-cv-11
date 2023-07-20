"""폴더를 입력받아 얼굴을 탐지/정렬하는 스크립트"""
from facenet_pytorch import MTCNN
import torch
import mmcv, cv2
import numpy as np
import PIL
from PIL import Image
import os
from typing import List

import argparse
import math
from glob import glob

from tqdm import tqdm
from torchvision.utils import save_image

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--device', type=str, default='cuda:0')
    parser.add_argument('--load_path', type=str, default="/opt/ml/deepfake/data/celeb-df/meta_test/mobilefaseswap" )
    parser.add_argument('--save_path', type=str, default="/opt/ml/deepfake/data/celeb-df/meta_test/mobilefaseswap_aligned" )
    parser.add_argument('--img_size', type=int, default=160)
    parser.add_argument('--margin', type=int, default=0.1) #얼굴 주변에 마진 추가
    # parser.add_argument('--prob', type=float, default=0.95)
    parser.add_argument('--fps', type=int, default=5)
    # parser.add_argument('--align', action='store_true')
    parser.add_argument('--keep_all', action='store_true')

    args = parser.parse_args()

    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path, exist_ok=False)
    
    return args


class ExtractAndAlignFace:
    def __init__(self, args):
        self.args = args
        self.device = torch.device(args.device)
        self.path_list = os.listdir(args.load_path)
        self.path_list.sort()
        self.mtcnn = MTCNN(keep_all=args.keep_all,
                           image_size=args.img_size,
                           margin = args.margin,
                            device=self.device, post_process=False)

    def euclidean_distance(self, a, b):
        x1 = a[0]
        y1 = a[1]
        x2 = b[0]
        y2 = b[1]

        return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))

    def get_rotation_angle(self, left_eye, right_eye):
        left_eye_x, left_eye_y = left_eye
        right_eye_x, right_eye_y = right_eye

        if left_eye_y < right_eye_y:
            point_3rd = (right_eye_x, left_eye_y)
            direction = -1 
        else:
            point_3rd = (left_eye_x, right_eye_y)
            direction = 1

        a = self.euclidean_distance(left_eye, point_3rd)
        b = self.euclidean_distance(right_eye, left_eye)
        c = self.euclidean_distance(right_eye, point_3rd)

        cos_a = (b*b + c*c - a*a)/(2*b*c)

        angle = np.arccos(cos_a)
        angle = (angle * 180) / math.pi

        if direction == -1:
            angle = 90 - angle

        return angle, direction

    def extract_and_align(self, frames):
        """이미지 리스트를 입력받아 이미지별 한 개의 얼굴을 추출한 결과를 텐서로 반환"""

        # 배치 처리로 수정
        batch_boxes, batch_probs, batch_points = self.mtcnn.detect(frames, landmarks=True)

        # 프레임에서 얼굴을 탐지하지 못한 경우 스킵
        mask = np.array([boxes is not None for boxes in batch_boxes])
        
        batch_boxes = batch_boxes[mask]
        batch_probs = batch_probs[mask]
        batch_points = batch_points[mask]

        # 프레임별로 best 얼굴 1개씩만 추출
        batch_faces = self.mtcnn.extract(frames, batch_boxes, save_path=None)
        # img = Image.fromarray(face.squeeze().permute(1,2,0).numpy().astype(np.uint8))

        # extraction_dict = dict()
        # for i, frame in enumerate(frames):
        #     print('\rTracking {} frame: {}'.format(name, i + 1), end='')

        #     # Detect faces
        #     try:
        #         batch_boxes, batch_probs, batch_points = self.mtcnn.detect(frame, landmarks=True)
        #         filter_idx = np.where(batch_probs > args.prob)[0]
        #         batch_boxes, batch_probs, batch_points = batch_boxes[filter_idx], batch_probs[filter_idx], batch_points[filter_idx]
            
        #         for j, (box, _, point) in enumerate(zip(batch_boxes, batch_probs, batch_points)):
        #             box = [box]
        #             face = self.mtcnn.extract(frame, box, save_path=None)
        #             left_eye, right_eye = point[:2]
        #             angle, direction = self.get_rotation_angle(left_eye, right_eye)
        #             img = Image.fromarray(face.squeeze().permute(1,2,0).numpy().astype(np.uint8))
        #             align_img = img.rotate(-direction*angle, resample=Image.Resampling.BICUBIC)

        #             if j not in extraction_dict:
        #                 extraction_dict[j] = []
                    
        #             extraction_dict[j].append(align_img)
        #     except:
        #         print(f'\nCannot Detect any face in frame #{i}')

        return batch_faces # extraction_dict

    def main(self):
        for video_paths in tqdm(self.path_list):
            video_path = os.path.join(args.load_path,video_paths)
            videos = os.listdir(video_path)
            for video in videos:
                name = video.split('.')[0]
                frame = os.path.join(video_path,video)

                frame = cv2.imread(frame)
                img_cv2 = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # 얼굴 추출: 정렬은 일단 제외
                face = self.extract_and_align(img_cv2)
            # 결과 저장
                if not os.path.exists(f'/opt/ml/deepfake/data/celeb-df/meta_test/mobilefaseswap_aligned/{video_paths}'):
                    os.makedirs(f'/opt/ml/deepfake/data/celeb-df/meta_test/mobilefaseswap_aligned/{video_paths}')
                save_image(face, f'/opt/ml/deepfake/data/celeb-df/meta_test/mobilefaseswap_aligned/{video_paths}/{name}.png', value_range=(0, 255), normalize=True)
        # frame = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]
        # extraction_dict = self.extract_and_align(frames, name)

        # idx_len = len(extraction_dict)
        # for idx in range(idx_len):
        #     for i, img in enumerate(extraction_dict[idx]):
        #         img.save(f'{self.args.save_path}/{name}_{idx}_{i}.png', 'PNG') #name : 영상이름, idx : identity index, i : 프레임 인덱스

if __name__=='__main__':
    args = parse_args()
    eaa = ExtractAndAlignFace(args)
    eaa.main()

