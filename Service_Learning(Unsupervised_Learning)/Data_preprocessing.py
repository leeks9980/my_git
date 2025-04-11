import toolbox as tb

img_path = 'C:/Users/leeks/mine/Service_Learning(Unsupervised_Learning)/원천데이터/TS1_시나노골드/당도A등급'
json_path = 'C:/Users/leeks/mine/Service_Learning(Unsupervised_Learning)/라벨링데이터/TL1_시나노골드'

#이미지 이름 과 세그메테이션 이름 딕션너리
Label = tb.Image_mask_area(img_path, json_path)

#탈락 이미지 선택
del_img = tb.del_img(img_path, Label)

#이미지 마스크 작업
tb.image_masking_anti_aliasing(img_path, del_img)