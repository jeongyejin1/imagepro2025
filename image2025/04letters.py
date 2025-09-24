import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
img = np.full((500,500,3), 255, dtype=np.uint8)

# sans-serif small
cv2.putText(img, "Plain", (50,30), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0))
# san-serif normal
cv2.putText(img, "Simplex", (50,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
# san-serif bold
cv2.putText(img, "Duplex", (50,110), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,0))
# san-serif normal 크게
cv2.putText(img, "Simplex X 2", (200,110), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0))

# sans-serif small
cv2.putText(img, "Serif plain", (50,180), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
# san-serif normal
cv2.putText(img, "Serif normal", (50,220), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
# san-serif bold
cv2.putText(img, "Serif bold", (50,260), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,0))
# san-serif normal 크게
cv2.putText(img, "serif plain X 2", (200,260), cv2.FONT_HERSHEY_TRIPLEX, 2, (0,0,0))


font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 지원 폰트 경로
font = ImageFont.truetype(font_path, 30)

# OpenCV → Pillow 변환
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(img_pil)
draw.text((50, 440), "정예진제작", font=font, fill=(0, 0, 255))  # RGB 색상

# 다시 OpenCV로 변환
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
# 한글 표시
cv2.putText(img, "정예진제작",(50, 440), cv2.FONT_HERSHEY_COMPLEX ,  1, (0,0,255))
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

cv2.imshow("Girl", img)
cv2.waitKey()
cv2.destroyAllWindows()
