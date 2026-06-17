import pandas as pd
import glob
import os

# 1. 파일 합치기 설정
# 파일들이 저장된 폴더 경로 (현재 파이썬 파일과 같은 폴더일 경우 '.' 사용)
input_path = r'C:\dev\pythonProject\Project1'
output_file = 'zigzag_total_dataset_labeled.xlsx'


def merge_and_label():
    print(">> 데이터 병합 및 라벨링을 시작합니다...")

    # 폴더 내 모든 zigzag_review_...xlsx 파일 가져오기
    all_files = glob.glob(os.path.join(input_path, "zigzag_review_*.xlsx"))

    if not all_files:
        print("❌ 합칠 엑셀 파일이 없습니다. 경로를 확인해주세요.")
        return

    df_list = []
    for f in all_files:
        temp_df = pd.read_excel(f)
        df_list.append(temp_df)

    # 하나로 합치기
    df = pd.concat(df_list, ignore_index=True)
    print(f">> 총 {len(df)}개의 로우(Row)를 합쳤습니다.")

    # 2. 데이터 정제 (중복 및 누락 제거)
    df = df.drop_duplicates(subset=['리뷰'])  # 중복 리뷰 제거
    df = df.dropna(subset=['리뷰', '별점'])  # 본문이나 별점 없는 행 제거
    print(f">> 중복 제거 후 {len(df)}개의 데이터가 남았습니다.")

    # 3. 스마트 라벨링 사전 정의 (정확도를 높이기 위한 단어장)
    pos_words = ['최고', '추천', '좋아요', '만족', '예뻐요', '예쁨', '핏', '재구매', '성공', '인생템', '감동', '탄탄']
    neg_words = ['아쉽', '실망', '느려', '늦게', '냄새', '실밥', '보풀', '반품', '환불', '별로', '작아요', '커요', '불편']

    def get_smart_label(row):
        text = str(row['리뷰'])
        rating = row['별점']

        # 감성 점수 계산
        pos_score = sum(1 for word in pos_words if word in text)
        neg_score = sum(1 for word in neg_words if word in text)

        # [라벨링 로직]
        # 1. 별점이 1, 2점이면 무조건 부정(0)
        if rating <= 2:
            return 0

        # 2. 별점이 4, 5점인 경우
        elif rating >= 4:
            # 긍정 단어가 더 많거나 같으면 긍정(1)
            if pos_score >= neg_score:
                return 1
            # 별점은 높은데 부정적인 단어가 확실히 많으면 부정(0)으로 전환
            else:
                return 0

        # 3. 별점 3점(중립) 처리
        else:
            # 3점은 데이터 오염을 막기 위해 '삭제 대상'으로 분류하거나, 점수차에 따라 결정
            if pos_score > neg_score:
                return 1
            elif neg_score > pos_score:
                return 0
            else:
                return -1  # 삭제용 표시

    # 라벨링 적용
    df['label'] = df.apply(get_smart_label, axis=1)

    # 4. 애매한 데이터(3점 중립 등) 제거
    final_df = df[df['label'] != -1].copy()

    # 5. 최종 저장
    final_df.to_excel(output_file, index=False)
    print(f"\n✅ 작업 완료!")
    print(f"   - 최종 파일명: {output_file}")
    print(f"   - 긍정(1) 개수: {len(final_df[final_df['label'] == 1])}")
    print(f"   - 부정(0) 개수: {len(final_df[final_df['label'] == 0])}")


if __name__ == "__main__":
    merge_and_label()