import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os

# 1. 엑셀 파일 불러오기
file_path = 'zigzag_balanced_data.xlsx'

# 파일이 실제로 있는지 확인 (에러 방지용)
if not os.path.exists(file_path):
    print(f"오류: '{file_path}' 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
else:
    df = pd.read_excel(file_path)

    # -------------------------------------------------------
    # 실제 라벨 컬럼명으로 수정 (예: 'label', 'score' 등)
    target_column = 'label'
    # -------------------------------------------------------

    # 2. 한글 폰트 설정
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':  # Mac
        plt.rc('font', family='AppleGothic')
    else:
        plt.rc('font', family='NanumGothic')

    plt.rcParams['axes.unicode_minus'] = False

    # 3. 데이터 개수 세기
    counts = df[target_column].value_counts().sort_index()

    # 4. 그래프 그리기
    plt.figure(figsize=(8, 6))

    # 막대 색상 설정 (0: 빨강/부정, 1: 파랑/긍정)
    colors = ['#ff6b6b', '#4dabf7']

    # 바 차트 생성
    bars = plt.bar(counts.index.astype(str), counts.values, color=colors, width=0.5)

    # 5. 막대 위에 숫자 표시하기
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}개',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    # 6. 그래프 꾸미기
    plt.title(f'최종 데이터셋 라벨 분포 (총 {len(df)}개)', fontsize=15)
    plt.xlabel('라벨 (0:부정, 1:긍정)', fontsize=12)
    plt.ylabel('리뷰 개수', fontsize=12)
    plt.xticks(ticks=[0, 1], labels=['부정 (0)', '긍정 (1)'])

    # -------------------------------------------------------
    # [핵심] 그래프 이미지로 저장하기
    # -------------------------------------------------------
    save_filename = 'label_distribution.png'

    # dpi=300: 고화질 저장
    # bbox_inches='tight': 여백 잘림 방지
    plt.savefig(save_filename, dpi=300, bbox_inches='tight')

    print(f"✅ 그래프가 '{save_filename}' 파일로 저장되었습니다!")

    # 화면에도 띄우고 싶다면 아래 주석을 해제하세요.
    # (주의: plt.show()를 먼저 하면 저장된 파일이 빈 화면으로 나올 수 있으므로 savefig 뒤에 써야 합니다)
    plt.show()