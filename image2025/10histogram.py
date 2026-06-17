# 2025.11.5 이미지처리 수업
# 히스토그램 노멀라이즈 (정규화)

import cv2
import matplotlib.pylab as plt

#흑백이미지의 히스토그램
img = cv2.imread('./img/mountain.jpg', cv2.IMREAD_GRAYSCALE)

hist = cv2.calcHist([img], [0], None, [256], [0,255])
plt.plot(hist)
plt.show()
print(hist.shape)
print(hist)

#컬러이미지의 히스토그램
img = cv2.imread('./img/mountain.jpg')
channels = cv2.split(img)
colors = ('b', 'a', 'r')
for(ch, color) in zip(channels, colors):
    print(ch)
    print(color)
    hist = cv2.calcHist([ch], [0], None, [256], [0,255])
    plt.plot(hist, color=color)

plt.show()

# cv2.imshow('org', img)
# cv2.waitKey()
# cv2.destroyAllWindows()