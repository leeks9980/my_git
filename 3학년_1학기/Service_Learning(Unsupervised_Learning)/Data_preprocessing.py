import toolbox as tb

j = 'json 폴더 경로'
img = '사진 폴더 경로'
masked_i = '전처리 이미지 저장 경로'

preprocessing = tb.image_preprocessing(img, j)

preprocessing.Image_mask_area()
print('완료')
preprocessing.masking(masked_i)
print('완료')
