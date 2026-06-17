import pandas as pd

# 1. 엑셀 파일 불러오기 (read_excel 사용)
# 파일명은 사용자분 파일명에 맞췄습니다.
df = pd.read_excel('zigzag_total_dataset_labeled.xlsx')

# -------------------------------------------------------
# [중요] 'label' 부분은 실제 엑셀 파일의 라벨 컬럼명으로 바꿔주셔야 합니다!
# 예: 'score', 'star', 'sentiment' 등
target_column = 'label'
# -------------------------------------------------------

# 2. 긍정과 부정 데이터 분리
# (0: 부정, 1: 긍정이라고 가정)
df_negative = df[df[target_column] == 0]
df_positive = df[df[target_column] == 1]

# 3. 긍정 데이터에서 부정 데이터 개수만큼만 랜덤 추출
# n=len(df_negative) : 부정 데이터 개수(1,798개)에 맞춤
df_positive_sampled = df_positive.sample(n=len(df_negative), random_state=42)

# 4. 데이터 합치기
df_balanced = pd.concat([df_negative, df_positive_sampled])

# 5. 순서 섞기 (셔플)
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

# 6. 결과 확인 (콘솔 출력)
print(f"최종 저장 개수: {len(df_balanced)}개")
print(df_balanced[target_column].value_counts())

# 7. 엑셀 파일로 저장하기 (to_excel 사용)
# index=False를 해야 불필요한 번호 열이 생기지 않습니다.
df_balanced.to_excel('zigzag_balanced_data.xlsx', index=False)

print("저장 완료! 'zigzag_balanced_data.xlsx' 파일을 확인해보세요.")