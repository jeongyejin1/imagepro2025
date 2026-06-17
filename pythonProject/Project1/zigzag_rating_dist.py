import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터 불러오기
file_path = 'zigzag_total_dataset_labeled.xlsx'
try:
    df = pd.read_excel(file_path)
    print(f">> 데이터 로드 성공: 총 {len(df)}개 리뷰")
except FileNotFoundError:
    print("❌ 엑셀 파일을 찾을 수 없습니다.")
    exit()

# 2. 평점 개수 세기 (1~5점)
# 1~5점 중 없는 점수가 있어도 0으로 표시되도록 설정
rating_counts = df['별점'].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)

print("\n📊 [평점별 리뷰 개수]")
print(rating_counts)

# 3. 그래프 그리기
plt.figure(figsize=(10, 6))

# 색상 설정 (예시 사진처럼: 빨강 -> 노랑 -> 파랑)
# 1점(빨강), 2점(주황), 3점(노랑), 4점(연두), 5점(파랑)
colors = ['#FF6B6B', '#FFD93D', '#FFC107', '#6BCB77', '#4D96FF']

bars = plt.bar(rating_counts.index, rating_counts.values, color=colors, edgecolor='black', alpha=0.8)

# 막대 위에 숫자 표시
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height,
             f'{int(height):,}개',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# 꾸미기
plt.title('전체 브랜드 평점별 리뷰 총 개수', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('평점', fontsize=12)
plt.ylabel('리뷰 개수', fontsize=12)
plt.xticks([1, 2, 3, 4, 5]) # X축을 1,2,3,4,5로 고정
plt.grid(axis='y', linestyle=':', alpha=0.5)

# 저장하기
save_name = 'total_rating_distribution.png'
plt.savefig(save_name, dpi=300)
print(f"\n✅ 그래프 저장 완료! '{save_name}' 파일을 확인하세요.")
plt.show()