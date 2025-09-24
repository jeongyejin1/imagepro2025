# 2025.9.24
# roi : region of interest
import cv2
import numpy as np
img = cv2.imread('./img/sunset.jpg')
x=320; y=150; w=50; h=50
cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0))

cv2.imshow("IMG", img)
cv2.waitKey()
cv2.destroyAllWindows()

roi = img[y:y+h, x:x+w]
print(roi.shape)
cv2.rectangle(roi, (0,0), (h-1, w-1), (0,0,255))

cv2.imshow("IMG", img)
cv2.waitKey()
cv2.destroyAllWindows()

x,y,w,h = cv2.selectROI("img", img, False)
print(x,y,w,h)
if w and h:
    roi = img[y:y+h, x:x+w]
    cv2.imshow("roi", roi)
    cv2.imwrite("sunsetroi.jpg", roi)
cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()