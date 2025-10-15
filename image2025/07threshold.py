# 2025.10.15
# 이미지 분석 수업: threshold
# threshold : 문턱값

import cv2
import numpy as np


img = cv2.imread('./img/gray_gradient.jpg', cv2.IMREAD_GRAYSCALE)
thresh_np = np.zeros_like(img)
# 중간숫자 : 127
# 첫번째방법
thresh_np[img>192] = 255
thresh_np[(img > 128) & (img <= 192)] = 128
thresh_np[(img > 64) & (img <= 128)] = 64

# 두번째방법
thresh_np = np.zeros_like(img)
thresh_np[img > 64] = 64
thresh_np[img > 128] = 128
thresh_np[img > 192] = 255

# 세번째방법
thresh_np = np.zeros_like(img)
print(img.shape)
ysize, xsize = img.shape
for x in range(xsize):
    for y in range(ysize):
        if(img[y, x] > 64):
            thresh_np[y, x] = 64
        if (img[y, x] > 128):
            thresh_np[y, x] = 128
        if (img[y, x] > 192):
            thresh_np[y, x] = 255

retval, thresh_cv = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)

cv2.imshow('thresh_np', thresh_np)
cv2.imshow("original", img)
cv2.imshow('cv thresh', thresh_cv)
cv2.waitKey()
cv2.destroyAllWindows()

# 실전에 적용 binary thrshold
img = cv2.imread("./img/scaned_paper.jpg", cv2.IMREAD_GRAYSCALE)
_, thresh_cv80 = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)
_, thresh_cv100 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
_, thresh_cv120 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
_, thresh_cv140 = cv2.threshold(img, 84, 255, cv2.THRESH_BINARY)
t, thresh_otsu = cv2.threshold(img, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imshow('cv thresh80', thresh_cv80)
cv2.imshow('cv thresh100', thresh_cv100)
cv2.imshow('cv thresh120', thresh_cv120)
cv2.imshow('cv thresh140', thresh_cv140)
cv2.imshow('cv otsu', thresh_otsu )
cv2.imshow('paper', img)
print(f'{t=}')
cv2.imshow('paper', img)
cv2.waitKey()
cv2.destroyAllWindows()

# 적응형 문턱값 적용 : 주위값에 따라 달라지게, blk_size = 9
blk_size = 9
C = 5
img = cv2.imread('./img/sudoku.jpg', cv2.IMREAD_GRAYSCALE)
t, thresh_otsu = cv2.threshold(img, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blk_size, C)
th2G = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blk_size, C)
th2M = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blk_size, C)
print(f'{t=}')
cv2.imshow('img', img)
cv2.imshow('ostu', thresh_otsu)
cv2.imshow('G', th2G)
cv2.imshow('M', th2M)
cv2.waitKey()
cv2.destroyAllWindows()