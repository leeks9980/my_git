import os
import cv2 #이미지 처리를 위한 라이브러리
from matplotlib import pyplot as plt #이미지 출력을 위한 라이브러리
import numpy as np
import json  #json파일을 읽기 위한 라이브러리
import shutil
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


class image_preprocessing:
    def __init__(self, img_path, json_path):
        self.img_path = img_path
        self.json_path = json_path

    #이미지 이름 리스트 만들기
    def Image_mask_area(self):
        #이미지 파일 이름 리스트
        os.chdir(self.img_path)   #작업환경 변경
        files_img = os.listdir(self.img_path) #폴더 안에 있는 것들 확인
        image_name_list = []

        for file in files_img:
            image_name_list.append(file)

        #json파일 이름 딕셔너리 만들기
        os.chdir(self.json_path)
        files_json = os.listdir(self.json_path)

        json_nema_list = [] #json파일명을 위한
        json_nema_and_img = {} #json파일명 과 이미지파일명 을 위한

        for file in files_json:
            json_nema_list.append(file)

        for json_nema in json_nema_list: 
            #께진 json을 걸러내기 위한 예외 처리
            try:
                with open(json_nema, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                json_nema_and_img[json_nema]=data['images']['img_file_name']
            except Exception: 
                pass

        #json파일에 segmentation 값 추출
        os.chdir(self.json_path)
        files_json = os.listdir(self.json_path)

        json_nema_and_segmentation = {} #json파일명 과 segmentation깂 을 위한

        for file in files_json:
            json_nema_list.append(file)

        for json_nema in json_nema_list: 
            #께진 json을 걸러내기 위한 예외 처리
            try:
                with open(json_nema, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                json_nema_and_segmentation[json_nema]=data["annotations"]["segmentation"]
            except Exception: 
                pass


        #이미지 파일과 json파일 1ㄷ1 매치
        img_and_json_Match = {}
        img_and_segmentation_Match = {}

        for img_name in image_name_list:
            for key, value in json_nema_and_img.items():
                if img_name == value:
                    img_and_json_Match[img_name] = key

        for key, value in img_and_json_Match.items():
            for key_1, value_1 in json_nema_and_segmentation.items():
                if value == key_1:
                    img_and_segmentation_Match[key] = value_1

        self.img_and_segmentation_Match = img_and_segmentation_Match

    #탈락 이미지 선별
    def del_img(self):
        os.chdir(self.img_path)
        del_img = []
        #직사각형 이미지 제거
        for img, segmentation in self.img_and_segmentation_Match.items():
            image = cv2.imread(img)
            image_shape_x, image_shape_y, a = image.shape
            if  image_shape_x != image_shape_y: 
                del_img.append(img)
        for img in del_img: 
            del self.img_and_segmentation_Match[img]


    #이미지 마스킹 작업
    def image_masking(self, save_path):
        self.save_path = save_path
        a = 0
        for img, segmentation in self.img_and_segmentation_Match.items():
            a = a + 1   
            # 이미지 불러오기
            os.chdir(self.img_path)
            image = cv2.imread(img)  # shape: (H, W, 3)

            # 세그멘테이션 좌표 준비
            segmentation_spot = np.array(segmentation, dtype=np.int32).reshape((-1, 2)) #(N, 2)의 2차원 배열로 바꾸는 것

            # 마스크 생성 (흰색이 객체 영역)
            mask = np.zeros(image.shape[:2], dtype=np.uint8) #image.shape[:2] 앞에 있는 2가지 값만 가져오기 
            cv2.fillPoly(mask, [segmentation_spot], 255)   #fillPoly(대상 이미지, 다격형 좌표, 색상(0~255)) 다각형 내부를 체워 주는 함수

            # 이미지 배경 제거
            masked_image = cv2.bitwise_and(image, image, mask=mask)   #bitwise_and(이미지1, 이미지2, 마스크) 마스크에 255값이 부분을 제외한 나머지 부분 제거
            resized = cv2.resize(masked_image, (128, 128)) #이미지 축소  , interpolation=cv2.INTER_AREA
            
            saved_path = os.path.join(save_path, f'output_{a}.png')  #저장 경로 설정
            #결과물 저장
            cv2.imwrite(saved_path, resized)

    def cnn_classification(self, output_clean_adress, output_dirty_adress, model_path):
        model = load_model(model_path)

        # 2. 경로 설정
        input_folder = self.save_path
        output_clean = output_clean_adress
        output_dirty = output_dirty_adress
        image_size = (124, 124)

        # 3. 출력 폴더 생성
        os.makedirs(output_clean, exist_ok=True)
        os.makedirs(output_dirty, exist_ok=True)

        # 4. 예측 및 저장
        dirty_count = 0
        total_count = 0

        for fname in os.listdir(input_folder):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                total_count += 1
                img_path = os.path.join(input_folder, fname)
                img = image.load_img(img_path, target_size=image_size)
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                prediction = model.predict(img_array, verbose=0)
                prob = prediction[0][0]

                if prob > 0.5:
                    dirty_count += 1
                    shutil.copy(img_path, os.path.join(output_dirty, fname))
                else:
                    shutil.copy(img_path, os.path.join(output_clean, fname))

        # 5. 통계 출력
        print(f"\n총 이미지 수: {total_count}장")
        print(f"불순물 없는 이미지 수: {dirty_count}장")
        print(f"정상 비율: {dirty_count / total_count:.2%}")


