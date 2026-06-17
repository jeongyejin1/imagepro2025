import cv2
import numpy as np

img_file = "./img/girl.jpg"
img = cv2.imread(img_file)
print(img.shape)

# BGR 공간을 YUV공간으로 변환
imgy = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
y, u, v = cv2.split(imgy)

cv2.imshow("girl", img)
cv2.imshow("imgy", y)
cv2.waitKey()
cv2.destroyAllWindows()

# 수식에 의해 y값을 직접 계산
imgyy = np.full((293, 406), 255, dtype=np.uint8)
b, g, r = cv2.split(img)
imgyy = 0.299 * r + 0.587 * g + 0.144 * b
imgyy = imgyy.astype(np.uint8)

# opencv 변환갑솨 직접 계산한 값의 차이 비교
diff = y - imgyy

print(diff)
cv2.imshow("diff", diff)
cv2.imshow("imgyy", imgyy)
cv2.waitKey()
cv2.destroyAllWindows()
