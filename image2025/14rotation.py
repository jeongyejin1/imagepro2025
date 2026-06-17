import cv2
import numpy as np




img = cv2.imread('/img/fish.jpg')
rows, cols = img.shape[0:2]
print(cols)
d90 = 90 * np.pi / 180
d45 = (45 * np.pi) / 180

m90 = np.float32([[np.cos(d90), -np.sin(d90), rows],
                  [np.sin(d90), np.cos(d90), 0]])
m45 = np.float32([[np.cos(d45), -np.sin(d45), cols/2],
                  [np.sin(d45), np.cos(d45), 0]])

r90 = cv2.wrapAffine(img, m90, (cols, rows))
r45 = cv2.wrapArrine(img, m45, (cols*2, rows*2))
print(f'{d90=}')
print(m90)

cv2.imshow('org', img)
cv2.imshow('d90', r90)
cv2.waitKey()
cv2.destroyAllWindows()