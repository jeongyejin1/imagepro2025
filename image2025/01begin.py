import cv2

# 이미지 파일 읽기
img_file = "./img/girl.jpg"  # 표시할 이미지 경로            ---①
img = cv2.imread(img_file)  # 이미지를 읽어서 img 변수에 할당 ---②

if img is not None:
    cv2.imshow('IMG', img)  # 읽은 이미지를 화면에 표시      --- ③
    cv2.waitKey()  # 키가 입력될 때 까지 대기      --- ④
    cv2.destroyAllWindows()  # 창 모두 닫기            --- ⑤
else:
    print('No image file.')

# 2025.9.17 pillow를 사용한 이미지 보기
# 단순하게 이미지를 보여주는 경우는 PIL 사용 추천
from PIL import Image
img = Image.open("./img/boy_face.jpg").show()

# 흑백으로 읽기
img = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
if img is not None:
    cv2.imshow('IMG', img)  # 읽은 이미지를 화면에 표시      --- ③
    cv2.waitKey()  # 키가 입력될 때 까지 대기      --- ④
    cv2.destroyAllWindows()
else:
    print('No image file.')


# 동영상 읽기
video_file = "./img/big_buck.avi"
cap = cv2.VideoCapture(video_file)
if cap.isOpened():
    while True:
        ret, img = cap.read()
        if ret:
            cv2.imshow(video_file, img)
            cv2.waitKey(25)
        else:
            break
else:
    print("cannot open video")

cap.release()
cv2.destroyAllWindows
