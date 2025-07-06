from ultralytics import YOLO
import cv2

# 모델 로드
model = YOLO("C:/Users/leeks/mine/Wrinkle-Detection-StreamLit/best.pt")  # YOLOv8으로 학습된 주름 탐지 모델

# 테스트 이미지 경로
img_path = "D:/028.한국인 피부상태 측정 데이터/3.개방데이터/1.데이터/Training/01.원천데이터/TS/3. 스마트폰/0002/0002_03_F.jpg"

# 추론 수행
results = model(img_path)

# 결과 시각화
results[0].show()  # OpenCV 창으로 보여줌
results[0].save(save_dir="results/")  # 결과 이미지 저장
