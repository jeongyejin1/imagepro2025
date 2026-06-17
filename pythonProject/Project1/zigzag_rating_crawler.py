import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

# ==========================================
# [설정] 지그재그 상품 URL 리스트
TARGET_URLS = [
    # 1.슬로우앤드 (레이어드셔츠, 나시 , 슬랙스, 데님팬츠: 884개 ->2794개 추출)
    #"https://zigzag.kr/catalog/products/127356723",
    #"https://zigzag.kr/catalog/products/135006673"
    #"https://zigzag.kr/catalog/products/119829258"
    # 2.고고싱 (슬랙스:1004개, 니트:1000개, 데님팬츠:1003개 -> 3007개 추출)
    #"https://zigzag.kr/catalog/products/140751630"
    #"https://zigzag.kr/catalog/products/134111551"
    #"https://zigzag.kr/catalog/products/123099184"
    # 3.블랙업 ( 슬랙스: 1003개, 긴팔티:1000개, 부츠컷데님팬츠:835개 -> 2838개 추출)
    #"https://zigzag.kr/catalog/products/100119896"
    #"https://zigzag.kr/catalog/products/127456743"
    #"https://zigzag.kr/catalog/products/129133636"
    # 4.육육걸즈 ( 데님팬츠: 633개,반팔티:394개,트레이닝팬츠:940개, 나시: 526개 -> 2523개 추출)
    #"https://zigzag.kr/catalog/products/100408842"
    #"https://zigzag.kr/catalog/products/100511186"
    #"https://zigzag.kr/catalog/products/120497545"
    #"https://zigzag.kr/catalog/products/105657134"
    # 5. 베니토 (부츠컷 슬랙스:1000개, 니트: 466개, 반팔티:456개 , 블라우스:810개 -> 2732개
    #"https://zigzag.kr/catalog/products/101062215"
    #"https://zigzag.kr/catalog/products/133185968"
    #"https://zigzag.kr/catalog/products/111411935"
    #"https://zigzag.kr/catalog/products/100424661"
    # 6. 베이델리 ( 데님팬츠:1008개, 니트:1004개, 트레이닝팬츠:1005개 -> 3017개
    #"https://zigzag.kr/catalog/products/134770445"
    #"https://zigzag.kr/catalog/products/150922802"
    #"https://zigzag.kr/catalog/products/135012008"
    # 7. 어텀 (니트:1008 , 와이드팬츠: 1008 ,티셔츠:937개 -> 2953개
    #"https://zigzag.kr/catalog/products/131059251"
    #"https://zigzag.kr/catalog/products/137691186"
    #"https://zigzag.kr/catalog/products/108222216"
    # 8. 핫핑 ( 니트:1003개 , 슬랙스:1008개 , 긴팔티 :1002개 ->3013
    #"https://zigzag.kr/catalog/products/131967482"
    #"https://zigzag.kr/catalog/products/147654541"
    #"https://zigzag.kr/catalog/products/103347769"

]

# 목표 리뷰 수
REVIEWS_PER_PRODUCT = 1000


# ==========================================

def crawl_zigzag_product(driver, url, target_count):
    print(f"\n>> [지그재그 접속] {url}")
    try:
        driver.get(url)
        time.sleep(random.uniform(3, 5))

        # ---------------------------------------------------------
        # [단계 1] '리뷰' 탭 클릭
        # ---------------------------------------------------------
        if "review/list" not in url:
            print("   ㄴ 1. '리뷰' 탭 이동 중...")
            try:
                driver.execute_script("window.scrollTo(0, 500);")
                time.sleep(1)

                review_tab = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-custom-ta-key*='PDP_REVIEW_TAB']"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", review_tab)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", review_tab)
                time.sleep(2)
            except:
                print("      (탭 클릭 패스)")

            # ---------------------------------------------------------
            # [단계 2] '리뷰 전체보기' 클릭 (포토 제외)
            # ---------------------------------------------------------
            print("   ㄴ 2. '리뷰 전체보기' 버튼 클릭 시도...")
            try:
                see_all_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., '리뷰 전체보기') and not(contains(., '포토'))]"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", see_all_btn)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", see_all_btn)
                print("      -> 클릭 성공! 리스트 로딩 중...")
                time.sleep(3)
            except:
                print("      (버튼 클릭 실패 또는 이미 진입함)")

        # ---------------------------------------------------------
        # [단계 3] 데이터 수집 (별점 포함)
        # ---------------------------------------------------------
        print(f"   ㄴ 3. 데이터 수집 시작 (목표: {target_count}개)...")

        collected_reviews = []
        scroll_stuck_count = 0
        prev_len = 0

        while True:
            # 1) 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.0)

            # 2) "더보기" 버튼 클릭
            try:
                more_buttons = driver.find_elements(By.CSS_SELECTOR, "div[data-review-feed-index] p")
                valid_buttons = [btn for btn in more_buttons if btn.text.strip() == "더보기"]
                if valid_buttons:
                    driver.execute_script("arguments[0].forEach(function(btn) { btn.click(); });", valid_buttons)
                    time.sleep(0.5)
            except:
                pass

            # 3) 데이터 추출
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_cards = soup.find_all("div", attrs={"data-review-feed-index": True})

            for card in review_cards:
                try:
                    # --- [별점 추출 로직 추가] ---
                    rating = 0
                    try:
                        # 별 아이콘(SVG)을 모두 찾습니다.
                        stars = card.find_all("svg", attrs={"data-zds-icon": "IconStarSolid"})
                        for s in stars:
                            # 스타일 속성에 'yellow' 색상이 있으면 칠해진 별입니다.
                            # (지그재그 노란색: var(--zds-color-palette-yellow-300))
                            style_attr = s.get("style", "")
                            if "yellow" in style_attr:
                                rating += 1

                        # 만약 별점을 못 찾았으면 기본값 5점으로 처리 (안전장치)
                        if rating == 0: rating = 5
                    except:
                        rating = 5  # 에러 시 기본값
                    # ---------------------------

                    # 본문 추출
                    content_span = card.find("span", class_=lambda x: x and "ebrcgb90" in x)
                    if not content_span:
                        more_btn = card.find("p", text="더보기")
                        if more_btn: content_span = more_btn.parent

                    if content_span:
                        full_text = content_span.get_text(" ", strip=True).replace("더보기", "").strip()

                        if len(full_text) > 10:
                            reviews_item = {
                                "url": url,
                                "별점": rating,  # 별점 추가됨
                                "리뷰": full_text
                            }

                            is_duplicate = False
                            for item in collected_reviews:
                                if item['리뷰'] == full_text:
                                    is_duplicate = True
                                    break
                            if not is_duplicate:
                                collected_reviews.append(reviews_item)
                except:
                    continue

            # 4) 현황 출력
            current_len = len(collected_reviews)
            print(f"      ... 현재 수집된 개수: {current_len}개")

            if current_len >= target_count:
                print("   ㄴ 목표 수량 달성!")
                break

            # 5) 멈춤 감지 및 해결
            if current_len == prev_len:
                scroll_stuck_count += 1
                if scroll_stuck_count >= 10:
                    print("   ㄴ 더 이상 데이터가 없습니다.")
                    break

                # 강력한 흔들기
                driver.execute_script("window.scrollBy(0, -1000);")
                time.sleep(1.0)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3.0)
            else:
                scroll_stuck_count = 0

            prev_len = current_len

        print(f"   ✅ 최종 수집 완료: {len(collected_reviews)}개")
        return collected_reviews

    except Exception as e:
        print(f"   ❌ 에러 발생: {e}")
        return []


def main():
    print(f">> 지그재그 크롤링 시작 (총 {len(TARGET_URLS)}개 상품)")
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")

    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=142)
    except Exception as e:
        print(f"❌ 드라이버 오류: {e}")
        return

    try:
        for i, url in enumerate(TARGET_URLS):
            print(f"\n--- [{i + 1}/{len(TARGET_URLS)}] 번째 상품 ---")
            product_reviews = crawl_zigzag_product(driver, url, REVIEWS_PER_PRODUCT)

            if product_reviews:
                df = pd.DataFrame(product_reviews)
                df = df.drop_duplicates(subset=['리뷰'])

                try:
                    p_id = url.split('/')[-1]
                except:
                    p_id = f"product_{i}"
                filename = f"zigzag_review_{p_id}.xlsx"

                # 엑셀 저장
                df.to_excel(filename, index=False)
                print(f"💾 저장 완료: {filename} ({len(df)}개)")
            else:
                print("⚠️ 수집된 데이터가 없습니다.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()