import os
import cv2 #이미지 처리를 위한 라이브러리
from matplotlib import pyplot as plt #이미지 출력을 위한 라이브러리
import numpy as np
import json  #json파일을 읽기 위한 라이브러리

#파일 경로
img_path = 'C:/Users/leeks/mine/Service_Learning(Unsupervised_Learning)/원천데이터/TS1_시나노골드/당도A등급'
json_path = 'C:/Users/leeks/mine/Service_Learning(Unsupervised_Learning)/라벨링데이터/TL1_시나노골드'


#이미지 이름 리스트 만들기
def Image_mask_area(img_path, json_path):
    os.chdir(img_path)   #작업환경 변경
    files_img = os.listdir(img_path) #폴더 안에 있는 것들 확인
    image_name_list = []

    for file in files_img:
        image_name_list.append(file)

    #json파일 이름 딕셔너리 만들기
    os.chdir(json_path)
    files_json = os.listdir(json_path)

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
    os.chdir(json_path)
    files_json = os.listdir(json_path)

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
    return img_and_segmentation_Match


#이미지 마스킹 작업
def image_masking(img_and_segmentation_Match):
    for img, segmentation in img_and_segmentation_Match.items():
        # 이미지 불러오기
        os.chdir(img_path)
        image = cv2.imread(img)  # shape: (H, W, 3)

        # 세그멘테이션 좌표 준비
        segmentation_spot = np.array(segmentation, dtype=np.int32).reshape((-1, 2)) #(N, 2)의 2차원 배열로 바꾸는 것

        # 마스크 생성 (흰색이 객체 영역)
        mask = np.zeros(image.shape[:2], dtype=np.uint8) #image.shape[:2] 앞에 있는 2가지 값만 가져오기 
        cv2.fillPoly(mask, [segmentation_spot], 255)   #fillPoly(대상 이미지, 다격형 좌표, 색상(0~255)) 다각형 내부를 체워 주는 함수

        # 이미지 배경 제거
        masked_image = cv2.bitwise_and(image, image, mask=mask)   #bitwise_and(이미지1, 이미지2, 마스크) 마스크에 255값이 부분을 제외한 나머지 부분 제거
        resized = cv2.resize(masked_image, (256,256))  #resize(이미지, (원하는x,y)) x, y 값으로 사진의 크기를 줄임

        # 결과 보기
        cv2.imshow("Masked Image", resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()