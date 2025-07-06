import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_gabor(image, ksize=21, sigma=5.0, theta=0, lambd=10.0, gamma=0.5):
    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, 0, ktype=cv2.CV_32F)
    filtered = cv2.filter2D(image, cv2.CV_32F, kernel)
    return filtered

def normalize(img):
    img = img - img.min()
    img = img / (img.max() + 1e-5)
    img = (img * 255).astype(np.uint8)
    return img

def process_image(path):
    img = cv2.imread(path)
    if img is None:
        print("이미지를 불러올 수 없습니다.")
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # CLAHE 대비 향상
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # Gabor 필터 4방향 적용 후 최대값 사용
    responses = []
    for theta in [0, np.pi/4, np.pi/2, 3*np.pi/4]:
        filtered = apply_gabor(gray, theta=theta)
        responses.append(filtered)
    combined = np.maximum.reduce(responses)

    # 정규화
    norm_img = normalize(combined)

    # Otsu 임계값으로 이진화
    _, binary = cv2.threshold(norm_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 결과 출력
    plt.figure(figsize=(12,6))
    plt.subplot(1,3,1)
    plt.imshow(gray, cmap='gray')
    plt.title('CLAHE Grayscale')
    plt.axis('off')

    plt.subplot(1,3,2)
    plt.imshow(norm_img, cmap='gray')
    plt.title('Gabor Filtered')
    plt.axis('off')

    plt.subplot(1,3,3)
    plt.imshow(binary, cmap='gray')
    plt.title('Binary Mask (Otsu Threshold)')
    plt.axis('off')

    plt.show()

# 테스트할 이미지 경로
image_path = "Find_the_pores/0002_03_F.jpg"
process_image(image_path)
