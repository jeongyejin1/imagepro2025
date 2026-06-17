import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from kiwipiepy import Kiwi  # 자바 없이 실행 가능한 빠른 분석기
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import re

# =============================================================================
# 1. 설정 및 데이터 로드
# =============================================================================
# 한글 폰트 설정 (윈도우)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 파일 불러오기
file_path = 'zigzag_balanced_data.xlsx'  # 원본 파일명
print("1. 데이터를 불러오는 중입니다...")
df = pd.read_excel(file_path)

# ---------------------------------------------------------
# [쇼핑몰 매핑 로직] 사용자분이 주신 코드 그대로 적용
# ---------------------------------------------------------
mall_mapping = {
    '슬로우앤드': ['127356723', '135006673', '119829258'],
    '고고싱': ['140751630', '134111551', '123099184'],
    '블랙업': ['100119896', '127456743', '129133636'],
    '육육걸즈': ['100408842', '100511186', '120497545', '105657134'],
    '베니토': ['101062215', '133185968', '111411935', '100424661'],
    '베이델리': ['134770445', '150922802', '135012008'],
    '어텀': ['131059251', '137691186', '108222216'],
    '핫핑': ['131967482', '147654541', '103347769']
}

# URL에서 ID 추출하여 쇼핑몰 이름 매핑
# (에러 방지를 위해 url 컬럼을 문자열로 변환 후 처리)
if 'url' in df.columns:
    df['product_id'] = df['url'].astype(str).str.split('/').str[-1]

    # 매핑 딕셔너리 뒤집기 (ID -> 쇼핑몰이름)
    id_to_mall = {str(pid): mall for mall, ids in mall_mapping.items() for pid in ids}

    df['shopping_mall'] = df['product_id'].map(id_to_mall)

    # 매핑된 데이터만 남기기
    df_filtered = df.dropna(subset=['shopping_mall']).copy()
    print(f"   -> 쇼핑몰 매핑 완료! 분석 대상 리뷰 수: {len(df_filtered)}개")
else:
    print("!! 오류: 엑셀 파일에 'url' 컬럼이 없습니다. 컬럼명을 확인해주세요.")
    exit()

# =============================================================================
# 2. 텍스트 전처리 (Kiwi 사용)
# =============================================================================
kiwi = Kiwi()
stop_words = {
    '진짜', '너무', '정말', '완전', '그냥', '정도', '생각', '구매', '주문', '배송',
    '부분', '살짝', '조금', '마음', '보고', '느낌', '계속', '다른', '역시', '제일',
    '제품', '상품', '사람', '때문', '자체', '지금', '고민'
}


def preprocess(text):
    if not isinstance(text, str):
        return []
    # 1. 특수문자 제거 없이 Kiwi는 알아서 잘 처리하지만, 깔끔하게 하기 위해 유지
    text = re.sub(r'[^가-힣\s]', '', str(text))

    # 2. 형태소 분석
    tokens = kiwi.tokenize(text)

    # 3. 명사(N..)이면서 2글자 이상, 불용어 제외
    results = []
    for t in tokens:
        if t.tag.startswith('N') and len(t.form) > 1:
            if t.form not in stop_words:
                results.append(t.form)
    return results


print("2. 형태소 분석 및 토큰화 진행 중 (잠시만 기다려주세요)...")
# 실제 리뷰 컬럼명이 '리뷰'인지 'review_text'인지 확인 필요. 여기선 '리뷰'로 가정
review_col = '리뷰' if '리뷰' in df_filtered.columns else 'review_text'
df_filtered['processed_tokens'] = df_filtered[review_col].apply(preprocess)
print("   -> 전처리 완료!")


# =============================================================================
# 3. 토픽 모델링 & 워드클라우드 함수
# =============================================================================
def run_topic_modeling_and_save(tokens_list, mall_name, sentiment_label, color_map):
    # 데이터가 너무 적으면(10개 미만) 스킵
    if len(tokens_list) < 10:
        print(f"   [Pass] {mall_name} ({sentiment_label}): 데이터 부족 ({len(tokens_list)}개)")
        return

    # 1. CountVectorizer (텍스트 -> 숫자 벡터)
    # 이미 리스트로 되어있으므로 tokenizer, preprocessor는 dummy로 설정
    dummy = lambda x: x
    vectorizer = CountVectorizer(tokenizer=dummy, preprocessor=dummy, min_df=2)

    try:
        dtm = vectorizer.fit_transform(tokens_list)
    except ValueError:
        print(f"   [Pass] {mall_name} ({sentiment_label}): 유효한 단어 없음")
        return

    # 2. LDA (토픽 1개 추출 -> 가장 강력한 주제 찾기)
    lda = LatentDirichletAllocation(n_components=1, random_state=42)
    lda.fit(dtm)

    # 3. 단어 가중치 추출
    feature_names = vectorizer.get_feature_names_out()
    topic_dist = lda.components_[0]  # 첫 번째 토픽의 단어 분포

    # 단어:가중치 딕셔너리 생성
    word_dict = dict(zip(feature_names, topic_dist))

    # 상위 5개 키워드 텍스트로 뽑기 (제목 표시용)
    sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    top_keywords = ", ".join([w[0] for w in sorted_words])

    # 4. 워드클라우드 그리기
    wc = WordCloud(
        font_path='C:/Windows/Fonts/malgun.ttf',  # 폰트 경로
        background_color='white',
        width=600, height=400,
        colormap=color_map,  # 색상 테마
        max_words=30,  # 너무 난잡하지 않게 최대 30개만
        prefer_horizontal=0.9  # 가로로 출력
    )
    wc.generate_from_frequencies(word_dict)

    # 그래프 생성 및 저장
    plt.figure(figsize=(8, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    title_str = f"{mall_name} [{sentiment_label}]\n주요 키워드: {top_keywords}"
    plt.title(title_str, fontsize=15, fontweight='bold')

    # 파일명 저장 (예: 워드클라우드_슬로우앤드_긍정.png)
    filename = f"워드클라우드_{mall_name}_{sentiment_label}.png"
    plt.savefig(filename)
    plt.close()  # 메모리 해제

    print(f"   ✅ 저장 완료: {filename}")


# =============================================================================
# 4. 쇼핑몰별 반복 실행 (Main Loop)
# =============================================================================
mall_list = list(mall_mapping.keys())
print("\n3. 쇼핑몰별 긍/부정 분석 및 이미지 저장 시작\n" + "=" * 50)

for mall in mall_list:
    print(f"\nAnalyzing... [{mall}]")

    # 해당 쇼핑몰 데이터만 추출
    mall_data = df_filtered[df_filtered['shopping_mall'] == mall]

    # 1) 긍정 리뷰 (label == 1) -> 파란색 계열(Blues)
    pos_tokens = mall_data[mall_data['label'] == 1]['processed_tokens']
    run_topic_modeling_and_save(pos_tokens, mall, "긍정", "Blues")

    # 2) 부정 리뷰 (label == 0) -> 빨간색 계열(Reds)
    neg_tokens = mall_data[mall_data['label'] == 0]['processed_tokens']
    run_topic_modeling_and_save(neg_tokens, mall, "부정", "Reds")

print("\n" + "=" * 50)
print("모든 분석이 끝났습니다! 폴더에 생성된 .png 파일들을 확인해주세요.")