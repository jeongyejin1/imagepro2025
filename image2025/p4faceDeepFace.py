#2025.12.3
# 이미지처리수업 마지막시간
# 마지막프로젝트 얼굴인식 DeepFace
# 환경설정 추가
# p3 faceRetian 환경 + 다음을 추가
# pip install deepface
import time

import cv2
from deepface import DeepFace
import numpy as np

img_path = "./img/children.jpg"
img = cv2.imread(img_path)

# detector_backend: retinaface, yunet, centerface, mtcnn, opencv, ssd
faces = DeepFace.extract_faces(img_path=img_path,
                              detector_backend='mtcnn', enforce_detection=False)

print(faces)

for face in faces:
    facial_area = face['facial_area']
    x = facial_area['x']; y=facial_area['y']
    w = facial_area['w']; h = facial_area['h']
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
    cv2.putText(img, f"{face['confidence']:.3f}",
                (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0))


# 399, 91, 91, 116
cv2.rectangle(img, (399,91), (399+91, 91+116),(255,0,0), 2)
cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()

# 각 모델 비교
timing = []
backends = ['retinaface', 'yunet', 'centerface', 'mtcnn']
for engine in backends:
    img = cv2.imread(img_path)
    start = time.time()
    faces = DeepFace.extract_faces(img_path=img_path,
                                   detector_backend=engine, enforce_detection=False)

    end = time.time()
    timing.append(end-start)

print(timing)

import matplotlib.pyplot as plt
plt.bar(backends, timing, color='skyblue', alpha=0.7)
plt.xlabel("Engine")
plt.ylabel("RunTime")
plt.show()