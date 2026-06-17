# matrx에 의한 이미지의 변환 두번째 시간

import cv2
import numpy as np
img = cv2.imread('./img/fish.jpg')
rows, cols, _ = img.shape

mtrx_flipx = np.float32([[-1,0, cols],
                   [0, 1, 0]])

mtrx_flipy = np.float32([[1,0, rows],
                   [0, -1, rows]])

mtrx_flipxy = np.float32([[-1,0, cols],
                   [0, -1, rows]])

img1 = cv2.warpAffine(img, mtrx_flipx, (rows, cols))
img2 = cv2.warpAffine(img, mtrx_flipy, (rows, cols))
img3 = cv2.warpAffine(img, mtrx_flipxy, (rows, cols))

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('img3', img3)
cv2.waitKey()
cv2.destroyAllWindows()

# 좌우반전을 파이썬 프로그램으로
# for문 사용
img_flipx = np.zeros_like(img)
for x in range(cols):
    for y in range(rows):
        img_flipx[y,x]=img[y, cols-x-1]

# 배열연산 사용
arr_flipx = np.zeros_like(img)
for x in range(cols):
    arr_flipx[:, x] = img[:, cols-x-1]

cv2.imshow('flip', img_flipx)
cv2.imshow('arr flip', arr_flipx)
cv2.imshow('org', img)
cv2.waitKey()
cv2.destroyAllWindows()
