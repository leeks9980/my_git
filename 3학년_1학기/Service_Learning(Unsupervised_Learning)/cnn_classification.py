import os
import shutil
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# 1. 모델 불러오기
model = load_model('모델 명')

# 2. 경로 설정
input_folder =  "테스트 파일 경로"
output_clean = "분류 파일 경로(불순물 없는)"
output_dirty = "분류 파일 경로(불순물 있는)"
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
            label = "불순물 있음"
            dirty_count += 1
            shutil.copy(img_path, os.path.join(output_dirty, fname))
        else:
            label = "불순물 없음"
            shutil.copy(img_path, os.path.join(output_clean, fname))

        print(f"{fname} → {label} (예측 확률: {prob:.4f})")

# 5. 통계 출력
print(f"\n총 이미지 수: {total_count}장")
print(f"불순물 있는 이미지 수: {dirty_count}장")
print(f"불순물 비율: {dirty_count / total_count:.2%}")
