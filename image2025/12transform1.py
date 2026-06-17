import cv2
import numpy as np

img = cv2.imread('./img/fish.jpg')


print(img.shape)
rows, cols = img.shape[0:2]
print(rows)
print(cols)

# 쉬프트 데이터
dx = 100
dy = 50

mtrx = np.float32([[1,0,dx],
                    [0,1,dy]])

dst1 = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy))
dst2 = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy),
                      None, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, (255,0,0) )
dst3 = cv2.warpAffine(img, mtrx, (cols+dx, rows+dy),
                      None, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT )


cv2.imshow('fish', img)
cv2.imshow('dst1', dst1)
cv2.imshow('dst2', dst2)
cv2.imshow('dst3', dst3)
cv2.waitKey()
cv2.destroyAllWindows()

mtrx = np.float32([[2,0,0],
                    [0,3,0]])
big = cv2.warpAffine(img, mtrx, (cols * 2, rows * 3), None, cv2.INTER_CUBIC)

mtrx = np.float32([[0,5,0,0],
                    [0,0,3,0]])
small = cv2.warpAffine(img, mtrx, (cols, rows), None, cv2.INTER_CUBIC)

mtrx = np.float32([[1,1,0],
                    [0,1,0]])
quiz = cv2.warpAffine(img, mtrx, (cols, rows), None, cv2.INTER_CUBIC)

cv2.imshow('big', big)
cv2.imshow('small', small)
cv2.imshow('quiz', quiz)
cv2.waitKey()
