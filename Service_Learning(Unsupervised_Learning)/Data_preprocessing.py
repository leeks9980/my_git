import toolbox as tb

img_path = 'C:/Users/leeks/mine/Service_Learning(Unsupervised_Learning)/원천데이터/TS1_시나노골드/당도A등급'
json_path = 'C:/Users/leeks/mine/Service_Learning(Unsupervised_Learning)/라벨링데이터/TL1_시나노골드'

Label = tb.Image_mask_area(img_path, json_path)
tb.image_masking(Label)