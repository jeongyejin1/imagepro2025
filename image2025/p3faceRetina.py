import cv2
from retinaface import RetinaFace
import numpy as np
from PIL import ImageFont, ImageDraw, Image


# --- 한글 출력을 위한 함수 정의 (변경 없음) ---
def put_text_korean(img, text, position, font_size, color):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    try:
        # 윈도우 폰트 경로 (맑은 고딕)
        font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", font_size)
    except:
        font = ImageFont.load_default()

    draw.text(position, text, font=font, fill=color)

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


# ---------------------------------------------------------

img_path = "./img/image.webp"

# 1. 얼굴 인식 수행
faces = RetinaFace.detect_faces(img_path)
print("얼굴 인식 완료:", len(faces), "명 감지됨")

# 2. 이미지 불러오기 및 크기 확인
img = cv2.imread(img_path)
h, w, c = img.shape  # h: 높이, w: 너비, c: 채널

# 3. 얼굴에 사각형 그리기 루프
for key, face in faces.items():
    facial_area = face['facial_area']
    cv2.rectangle(img, (facial_area[0], facial_area[1]),
                  (facial_area[2], facial_area[3]), (255, 0, 0), 2)

    score_text = f"{face['score']:.3f}"
    cv2.putText(img, score_text,
                (facial_area[0], facial_area[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

# ==========================================================================
# [수정됨] 학번 이름 오른쪽 상단에 넣기
# ==========================================================================
my_text = "2021143019 홍도영"
my_font_size = 30
margin = 20  # 가장자리 여백

# 텍스트가 차지할 실제 너비를 계산합니다.
try:
    # 길이를 재기 위해 잠시 폰트를 로드합니다.
    font_temp = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", my_font_size)
    text_width = font_temp.getlength(my_text)
except:
    # 폰트를 못 찾으면 대략적인 값으로 설정 (혹시 모를 에러 방지)
    text_width = len(my_text) * my_font_size * 0.8

# 오른쪽 끝 좌표 계산: (전체 이미지 너비 - 텍스트 너비 - 여백)
x_pos = int(w - text_width - margin)
y_pos = margin  # 상단 여백

# 계산된 위치(x_pos, y_pos)에 빨간색(255,0,0)으로 글씨 쓰기
img = put_text_korean(img, my_text, (x_pos, y_pos), my_font_size, (255, 0, 0))
# ==========================================================================


cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()