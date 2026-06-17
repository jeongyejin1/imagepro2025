# 2025.11.26
# 이미지처리 filter -> edge

import cv2
import numpy as np

img = cv2.imread('./img/children.jpg', cv2.IMREAD_GRAYSCALE)



gx_kernel = np.array([[-1, 1]])
gy_kernel = np.array([[-1],[1]])
edge_gx = cv2.filter2D(img, -1, gx_kernel)
edge_gy = cv2.filter2D(img, -1, gy_kernel)

cv2.imshow('org', img)
cv2.imshow('x edge', edge_gx)
cv2.imshow('edge', edge_gy)
cv2.waitKey()
cv2.destroyAllWindows()

# Sobel
gx_s = np.array([[-1,0,1], [-2,0,-2], [-1,0,1]])
gy_s = np.array([[-1,-2,-1], [0,0,0], [1,2,1]])
edge_gxs = cv2.filter2D(img, -1, gx_s)
edge_gys = cv2.filter2D(img, -1, gy_s)
edge_gxys = edge_gxs + edge_gys

sobelx = cv2.Sobel(img, -1, 1, 0, ksize=3)
cv2.imshow('org', img)
cv2.imshow('edgex', edge_gxs)
cv2.imshow('edgey', edge_gys)
cv2.imshow('edgex sobel', sobelx)
cv2.imshow('edge xy', edge_gxs)
cv2.waitKey()
cv2.destroyAllWindows()

#Schar
gx_sh = np.array([[-3,0,3], [-10,0,10], [-3,0,3]])
gy_sh = np.array([[1,1,1], [1,1,1], [1,1,1]])
scharx = cv2.filter2D(img, -1, gx_sh)
schary = cv2.filter2D(img, -1, gy_sh)

# Laplacian

gx_l = np.array([[0,1,0], [1,-4,1], [0,1,0]])
edge_lap = cv2.filter2D(img, -1, gx_l)

# Canny
canny = cv2.Canny(img, 50, 150)

cv2.imshow('org', img)
cv2.imshow('shcarx', scharx)
cv2.imshow('schary', schary)
cv2.imshow('lap', edge_lap)
cv2.imshow('canny', canny)
cv2.waitKey()
cv2.destroyAllWindows()



