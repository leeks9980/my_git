from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# 이미지 제너레이터
train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_gen = train_datagen.flow_from_directory(
    "파일 경로",
    target_size=(124, 124),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

val_gen = train_datagen.flow_from_directory(
    "파일 경로",
    target_size=(124, 124),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

# 클래스 비율 기반 가중치 계산
labels = train_gen.classes
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(labels), y=labels)
class_weight = dict(enumerate(class_weights))

# 모델 구성
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(124, 124, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(1, activation='sigmoid')  # 이진 분류
])

# 컴파일
model.compile(optimizer=Adam(learning_rate=0.00005), loss='binary_crossentropy', metrics=['accuracy'])

# 학습
model.fit(train_gen, validation_data=val_gen, epochs=100, class_weight=class_weight)

#모델 저장
#model.save('apple_classifier.h5')