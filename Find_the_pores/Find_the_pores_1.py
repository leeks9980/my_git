import cv2
import numpy as np

def detect_pores_in_tile(tile):
    # 전처리
    gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    equalized = cv2.equalizeHist(blur)
    laplacian = cv2.Laplacian(equalized, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    _, thresh = cv2.threshold(laplacian, 20, 255, cv2.THRESH_BINARY)

    # 윤곽선 검출
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pores = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 1 < area < 100:  # 모공 크기 범위
            pores.append(cnt)
    return pores

# 1. 원본 이미지 불러오기
img = cv2.imread("Find_the_pores\KakaoTalk_20250706_161547231.jpg")
h, w = img.shape[:2]

# 2. 분할할 타일 수 설정 (예: 3x3 분할)
tile_rows, tile_cols = 3, 3
tile_height = h // tile_rows
tile_width = w // tile_cols

# 3. 전체 결과 그릴 복사본 생성
output = img.copy()

# 4. 각 타일별 모공 검출 및 시각화
for i in range(tile_rows):
    for j in range(tile_cols):
        y1, y2 = i * tile_height, (i + 1) * tile_height
        x1, x2 = j * tile_width, (j + 1) * tile_width

        tile = img[y1:y2, x1:x2]
        pores = detect_pores_in_tile(tile)

        # 타일 좌표에 맞춰 이동시킨 후 그리기
        for cnt in pores:
            cnt_shifted = cnt + [x1, y1]  # 타일 위치만큼 이동
            cv2.drawContours(output, [cnt_shifted], -1, (0, 255, 0), 1)

# 5. 최종 결과 시각화
cv2.imshow("Detected Pores (Tiled)", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
