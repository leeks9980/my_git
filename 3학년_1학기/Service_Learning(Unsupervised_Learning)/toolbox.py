import os
import cv2 #이미지 처리를 위한 라이브러리
from matplotlib import pyplot as plt #이미지 출력을 위한 라이브러리
import numpy as np
import json  #json파일을 읽기 위한 라이브러리

#이미지 이름 리스트 만들기
def Image_mask_area(img_path, json_path):
    #이미지 파일 이름 리스트
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

#탈락 이미지 선별
def del_img(img_path, img_and_segmentation_Match):
    os.chdir(img_path)
    del_img = []
    #직사각형 이미지 제거
    for img, segmentation in img_and_segmentation_Match.items():
        image = cv2.imread(img)
        image_shape_x, image_shape_y, a = image.shape
        if  image_shape_x != image_shape_y: 
            del_img.append(img)
    for img in del_img: 
        del img_and_segmentation_Match[img]
    return img_and_segmentation_Match


#이미지 마스킹 작업
def image_masking_anti_aliasing(img_path, img_and_segmentation_Match):
    a = 0
    for img, segmentation in img_and_segmentation_Match.items():
        a = a + 1   
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
        resized = cv2.resize(masked_image, (128, 128)) #이미지 축소 및 안티 엘리어싱 , interpolation=cv2.INTER_AREA

        #결과물 저장
        cv2.imwrite(f'/Service_Learning(Unsupervised_Learning)/test/output_{a}.png', resized)
        
        # 결과 보기
        #cv2.imshow("Masked Image", resized)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

#이물질 탐지(미완성)
def foreign_object_detection(img_path):
    image = cv2.imread(img_path)
    resized = cv2.resize(image, (64, 64))

    height, width, a = resized.shape 

    zero_matrix = np.zeros((128, 128))
    
    for x in range(height):
        for y in range(width):
            neighbors = [   #이웃 픽셀 리스트
                (x-1, y-1), (x-1, y), (x-1, y+1),  # 상좌, 상, 상우
                (x, y-1), (x, y+1),                # 좌, 우
                (x+1, y-1), (x+1, y), (x+1, y+1)   # 하좌, 하, 하우
            ]
            for n_x, n_y in neighbors:  #이웃 픽셀 불러오기
                if 0 <= n_x < 64 and 0 <= n_y < 64:  # 경계 체크 
                    current_pixel = resized[x, y].astype(int) #overflow 방지용
                    neighbor_pixel = resized[n_x, n_y].astype(int) #overflow 방지용
                    if sum(current_pixel) != 0 and sum(neighbor_pixel) != 0: #검정색 부분 넘기기
                            if sum(current_pixel)/3 <= sum(neighbor_pixel)/3 - 45: #이상치 탐지(?)
                                resized[x, y] = [0,0,255]
                                zero_matrix[x, y] = 1 #분산을 구하기 위한 푯

    zero_matrix = zero_matrix.reshape(-1)
    if np.var(zero_matrix) >= 300: #분산값 으로 나뭇가지 식별
        print('나뭇가지',img_path)