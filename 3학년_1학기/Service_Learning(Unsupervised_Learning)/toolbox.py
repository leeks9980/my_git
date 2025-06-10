import os
import json  #json파일을 읽기 위한 라이브러리
import shutil
import torch
from torchvision import models, transforms
from PIL import Image, ImageDraw
import torch.nn.functional as F
import numpy as np
from PIL import UnidentifiedImageError
import cv2
class image_preprocessing:
    def __init__(self, img_path, json_path):
        self.img_path = img_path
        self.json_path = json_path

    #이미지 이름 리스트 만들기
    def Image_mask_area(self):
        self.img_and_segmentation_Match = {}

        for filename in os.listdir(self.json_path):
            path = os.path.join(self.json_path, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                img_name = data["images"]["img_file_name"]
                segmentation = data["annotations"]["segmentation"]
                
                if img_name and segmentation:
                    self.img_and_segmentation_Match[img_name] = {'smt':segmentation}

            except (json.JSONDecodeError, KeyError, FileNotFoundError): # 깨진 JSON, 키 없음, 파일 없음 등 무시
                continue 

    def masking(self, masked_img_dir):
        n = 0
        for i,j in self.img_and_segmentation_Match.items():
            #이미지 호출
            img_path = os.path.join(self.img_path, i)
            o_img = cv2.imread(img_path)
            
            if o_img is None:
                continue
                
            #json에 있는 경계 정보 가져오기
            points = np.array(j['smt'], dtype=np.float32).reshape(-1,2)
            
            #마스크 생성
            H, W, c = o_img.shape
            blank = np.zeros((H, W), dtype=np.uint8)

            int_points = np.round(points).astype(np.int32)
            cv2.fillPoly(blank, [int_points], 255)

            smooth_mask = cv2.GaussianBlur(blank, (15, 15), 0)

            tensor_mask = torch.from_numpy(smooth_mask).unsqueeze(0).unsqueeze(0).float().cuda() / 255.0

            mask_np = tensor_mask.squeeze().cpu().numpy()  # shape: (H, W)
            mask_np = np.expand_dims(mask_np, axis=2)      # shape: (H, W, 1)
            mask_np = np.repeat(mask_np, 3, axis=2)        # shape: (H, W, 3) - RGB 채널에 맞춤
            
            #마스킹 작업 
            m_img = (o_img * mask_np).astype(np.uint8)
            n += 1
            
            #이미지 저장
            save_path = os.path.join(masked_img_dir, i)
            cv2.imwrite(save_path, m_img)