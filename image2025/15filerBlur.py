# 2025.11.19
# 이미지분석 -> 필터 -> 블러

import cv2
import numpy as np

img = cv2.imread('./img/gaussian_noise.jpg')

kernel = np.ones((5,5))/25
k1 = np.array([[1,2,1],[2,4,2],[1,2,1]]) / 16
print(kernel)
blured = cv2.filter2D(img, -1, kernel)
gblured = cv2.filter2D(img, -1, k1)
cv2.imshow('org', img)
cv2.imshow('blured', blured)
cv2.imshow('gblured', gblured)
cv2.waitKey()
cv2.destroyAllWindows()

# 2025.11.26
# 이미지분석 -> 필터 -> 가우시안, 메디안 median

# 가우시안 커널
k2 = cv2.getGaussianKernel(5, 0)
print(k2)
blur2 = cv2.filter2D(img, -1, k2 * k2.T)
print(k2 * k2.T)

# 가우시안 블러를 직접
blur3 = cv2.GaussianBlur(img, (3,3), 0)

# median blur
blur4 = cv2.medianBlur(img, 5)

# bilateral blur
blur5 = cv2.bilateralFilter(img, 5, 75, 75)

imgmerge = np.hstack((img, blur4, blur5))
cv2.imshow('all', imgmerge)
cv2.waitKey()
cv2.destroyAllWindows()
