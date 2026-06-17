import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# 자바 설치 필요 없는 Kiwi 분석기 사용
from kiwipiepy import Kiwi
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 설정 및 데이터 로드
file_path = 'zigzag_total_dataset_labeled.xlsx'
try:
    df = pd.read_excel(file_path)
    print(">> 데이터 로드 성공!")
except FileNotFoundError:
    print("❌ 엑셀 파일을 찾을 수 없습니다.")
    exit()

# 쇼핑몰 매핑
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

# ID 추출 및 매핑
if 'url' in df.columns:
    df['product_id'] = df['url'].str.split('/').str[-1].astype(str)
id_to_mall = {str(pid): mall for mall, ids in mall_mapping.items() for pid in ids}
df['shopping_mall'] = df['product_id'].map(id_to_mall)
df = df.dropna(subset=['shopping_mall'])

# ---------------------------------------------------------
# 2. 텍스트 전처리 (강력한 불용어 처리)
# ---------------------------------------------------------
kiwi = Kiwi()

# [핵심] 분석에 방해되는 단어들을 여기에 다 넣어주세요!
stop_words = [
    '진짜', '너무', '정말', '완전', '그냥', '정도', '생각', '구매', '주문', '배송',
    '부분', '살짝', '조금', '마음', '보고', '느낌', '계속', '다른', '역시', '제일',
    '사진', '화면', '모델', '후기', '리뷰', '사람', '때문', '이번', '고민', '만족',
    '도착', '하루', '총알', '기사', '포장', '상태'  # 배송 관련 단어도 긍정 토픽에서 제외하고 싶으면 추가
]


def preprocess(text):
    text = re.sub(r'[^가-힣\s]', '', str(text))
    tokens = kiwi.tokenize(text)
    # 일반 명사(NNG), 고유 명사(NNP)만 추출
    nouns = [t.form for t in tokens if t.tag in ['NNG', 'NNP']]
    return [n for n in nouns if len(n) > 1 and n not in stop_words]


print(">> 형태소 분석 및 불용어 제거 중... (잠시만 기다려주세요)")
df['processed_tokens'] = df['리뷰'].apply(preprocess)
print(">> 전처리 완료! 깔끔한 워드클라우드를 생성합니다.\n")


# ---------------------------------------------------------
# 3. 간결한 워드클라우드 생성 함수
# ---------------------------------------------------------
def run_topic_modeling_clean(tokens_list, title, color_map):
    if len(tokens_list) < 10: return

    dummy = lambda x: x
    vectorizer = CountVectorizer(tokenizer=dummy, preprocessor=dummy, min_df=3)
    dtm = vectorizer.fit_transform(tokens_list)

    # 토픽 1개로 핵심만 추출
    lda = LatentDirichletAllocation(n_components=1, random_state=42)
    lda.fit(dtm)

    feature_names = vectorizer.get_feature_names_out()
    topic_dist = lda.components_[0]
    word_dict = dict(zip(feature_names, topic_dist))

    # [핵심] 상위 10개 단어만 추출하여 워드클라우드에 전달
    sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    top_word_dict = dict(sorted_words)
    top_keywords = ", ".join([w[0] for w in sorted_words[:5]])  # 제목용 5개

    # max_words=20으로 설정하여 최대 20개까지만 그리도록 제한
    wc = WordCloud(font_path='malgun.ttf', background_color='white',
                   width=600, height=400, colormap=color_map,
                   max_words=20)
    wc.generate_from_frequencies(top_word_dict)

    plt.figure(figsize=(6, 4))  # 그림 크기도 아담하게
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"{title}\n(핵심: {top_keywords})", fontsize=12)

    filename = "clean_" + title.replace(" ", "_").replace("(", "").replace(")", "") + ".png"
    plt.savefig(filename, bbox_inches='tight')  # 여백 없이 깔끔하게 저장
    plt.close()
    print(f"   📄 저장 완료: {filename} -> 핵심: [{top_keywords}]")


# ---------------------------------------------------------
# 4. 실행 루프
# ---------------------------------------------------------
mall_list = list(mall_mapping.keys())

for mall in mall_list:
    print(f"\n🔍 Analyzing... [{mall}]")
    mall_data = df[df['shopping_mall'] == mall]

    pos_tokens = mall_data[mall_data['label'] == 1]['processed_tokens']
    run_topic_modeling_clean(pos_tokens, f"{mall} (긍정)", "viridis")  # 깔끔한 파란색 계열

    neg_tokens = mall_data[mall_data['label'] == 0]['processed_tokens']
    if len(neg_tokens) > 5:
        run_topic_modeling_clean(neg_tokens, f"{mall} (부정)", "inferno")  # 붉은색 계열
    else:
        print(f"   Skip: {mall}은 부정 리뷰가 너무 적습니다.")

print("\n✅ 모든 분석이 끝났습니다! 'clean_'으로 시작하는 파일들을 확인하세요.")