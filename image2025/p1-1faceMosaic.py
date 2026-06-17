# 얼굴 인식후 모자이크 처리: 익명화


import cv2

# 얼굴 검출
face_cascade = cv2.CascadeClassifier('./redata/haarcascade_frontalface_default.xml')



img = cv2.imread('./img/image.webp ')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray)



# 얼굴검출 후 모자이크
for face in faces:
    fx, fy, fw, fh = face
    roi = img[fx:fx+fh, fx:fx+fw]
    roi = cv2.resize(roi, (fw//10, fh//10))
    roi = cv2.resize(roi, (fw, fh))
    img[fy:fy + fh, fx:fx + fw] = roi


cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()