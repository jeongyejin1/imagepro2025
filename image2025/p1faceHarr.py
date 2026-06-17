# 얼굴인식 프로젝트
# opencv Harr filter를 연속적용하는 방식
# 2025.10.1
# 필터 다운로드 사이트
# https://github.com/opencv/opencv/tree/master/data/haarcascades

import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
face_cascade = cv2.CascadeClassifier('./redata/haarcascade_frontalface_default.xml')


# 눈 검출
eye_cascade = cv2.CascadeClassifier('./redata/haarcascade_eye.xml')


img = cv2.imread('./img/image.webp ')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray)

# [[146  96 120 120]
#  [398  97 106 106]]
print(faces)

# children.jpg
# cv2.rectangle(img, (146,96), (120,120), (255,0,0), 5)
# cv2.rectangle(img, (398,97), (106,106), (0,255,0), 5)

# boy_face.jpg
# cv2.rectangle(img, (146,190), (146+306,190+306), (0,255,0), 5)

# image.png
# cv2.rectangle(img, (276,68), (276+88,68+88), (0,255,0), 5)

# 네모를 일반적으로 표시
for face in faces:
    fx, fy, fw, fh = face
    cv2.rectangle(img, (fx, fy), (fx+fw, fy+fh), (0, 255, 0), 2)
    # 눈 검출 시작
    eyes = eye_cascade.detectMultiScale(gray[fy:fy+fh, fx:fx+fw])
    for eye in eyes:
        ex, ey, ew, eh = eye
        cv2.rectangle(img, (fx+ex, fy+ey), (fx+ex+ew, fy+ey+eh), (0, 0, 255), 2)

img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

font_path = "C:/Windows/Fonts/malgun.ttf"
font = ImageFont.truetype(font_path, 32)

draw = ImageDraw.Draw(img_pil)
draw.text((10, 10), "2023143038 정예진", font=font, fill=(255, 255, 255, 0))

img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)



cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()