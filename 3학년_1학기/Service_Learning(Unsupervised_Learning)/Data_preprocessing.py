import toolbox as tb

img_path = '이미지 파일 경로'
json_path = 'json 파일 경로'

dirty_path = "비정상 이미지 경로"
clean_path = "정상 이미지 경로"

model_path = "모델 경로" 

preprocessor = tb.image_preprocessing(img_path, json_path)

preprocessor.Image_mask_area()
preprocessor.del_img()
preprocessor.mask_and_classify()
