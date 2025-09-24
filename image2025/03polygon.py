import cv2
import numpy as np

img_file = "./img/girl.jpg"
img = cv2.imread(img_file)

cv2.rectangle(img, (50,50), (150,150), (255,0,0), 10)
cv2.rectangle(img, (300,300), (100,100), (0,255,0), 10)
cv2.rectangle(img, (450,200), (200,450), (0,0,255), 10)

cv2.imshow("Girl", img)
cv2.waitKey()
cv2.destroyAllWindows()

img = np.full((500,500,3), 255, dtype=np.uint8)

cv2.circle(img, (150,150), 100, (255,0,0))
cv2.circle(img, (300,150), 70, (0,255,0), 5)
cv2.circle(img, (450,200), 50, (0,0,255), -1)

cv2.imshow("Girl", img)
cv2.waitKey()
cv2.destroyAllWindows()

# 납작한 타원
cv2.ellipse(img, (325,300), (75, 50), 0, 0, 360, (255,0,0))
# 길쭉한 타원 - 아래 반원
cv2.ellipse(img, (450,300), (50, 75), 0, 0, 360, (255,0,255))

# 납작한 타원
cv2.ellipse(img, (50,425), (75, 50), 15, 0, 360, (255,0,0))
# 길쭉한 타원 - 아래 반원
cv2.ellipse(img, (200,425), (50, 75), 45, 0, 180, (255,0,255))

cv2.imshow("Girl", img)
cv2.waitKey()
cv2.destroyAllWindows()
