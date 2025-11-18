# main_crawler.py (댓글 시스템 로딩을 기다리는 진짜 최종 버전)

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 1. 크롤링할 정보 및 변수 설정
TARGET_WEBTOON_ID = '800770'
TOTAL_EPISODES = 180
early_episodes = list(range(1, 11))
mid_episodes = list(range(TOTAL_EPISODES // 2 - 4, TOTAL_EPISODES // 2 + 6))
late_episodes = list(range(TOTAL_EPISODES - 9, TOTAL_EPISODES + 1))
target_episodes = early_episodes + mid_episodes + late_episodes
max_comments_per_episode = 500

# 2. 크롬 드라이버 설정 및 쿠키 로그인
options = webdriver.ChromeOptions()
# options.add_argument('--headless') # 문제가 완전히 해결될 때까지 눈으로 직접 확인하세요.
options.add_argument('--disable-gpu')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

try:
    print("저장된 쿠키를 불러와 로그인합니다...")
    driver.get('https://www.naver.com')
    cookies = pd.read_pickle("naver_cookies.pkl")
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("✅ 쿠키 불러오기 성공!")
except Exception as e:
    print(f"❌ 쿠키 파일 로딩 실패: {e}")
    driver.quit()
    exit()

# 3. 댓글 수집 시작
all_comments = []
print(f">> 총 {len(target_episodes)}개 회차의 댓글 수집을 시작합니다.")

for episode_num in target_episodes:
    url = f"https://comic.naver.com/webtoon/detail?titleId={TARGET_WEBTOON_ID}&no={episode_num}"
    driver.get(url)
    print(f"--- {episode_num}화 댓글 수집 시작 (최대 {max_comments_per_episode}개) ---")

    try:
        # ★★★★★ 진짜 최종 해결책 ★★★★★
        # '더보기'를 찾기 전에, 댓글 영역 전체(id='comment')가 나타날 때까지 먼저 기다립니다.
        # 이 한 줄이 모든 문제의 핵심 해결책입니다.
        print("   ㄴ 댓글 시스템이 로딩될 때까지 대기합니다...")
        wait = WebDriverWait(driver, 15)  # 대기 시간을 15초로 넉넉하게 설정
        wait.until(EC.presence_of_element_located((By.ID, "comment")))
        print("   ㄴ 댓글 시스템 로딩 완료!")

        # '전체 보기' 버튼이 있다면 먼저 클릭
        try:
            unhide_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '전체')]")))
            unhide_button.click()
            print("   ㄴ '전체 보기' 버튼 클릭 성공!")
            time.sleep(1)
        except TimeoutException:
            print("   ㄴ '전체 보기' 버튼이 없어 바로 '더보기'를 시작합니다.")

        # '더보기' 버튼 계속 클릭
        comment_selector = 'p[class^="CommentBox_comment_text"]'
        while True:
            current_comments_count = len(driver.find_elements(By.CSS_SELECTOR, comment_selector))
            if current_comments_count >= max_comments_per_episode:
                print(f"   ㄴ 목표 댓글 수({max_comments_per_episode}개)에 도달하여 중단합니다.")
                break
            try:
                more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '더보기')]")))
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)
            except TimeoutException:
                print("   ㄴ '더보기' 버튼을 더 이상 찾을 수 없어 수집을 종료합니다.")
                break

        comments = driver.find_elements(By.CSS_SELECTOR, comment_selector)
        for comment in comments:
            all_comments.append({"회차": episode_num, "댓글": comment.text.strip()})
        print(f"✅ {episode_num}화 댓글 {len(comments)}개 수집 완료")

    except Exception as e:
        print(f"   ㄴ {episode_num}화 수집 중 알 수 없는 오류 발생: {e}")

# 4. 모든 작업 완료 후 브라우저 종료 및 파일 저장
driver.quit()

if all_comments:
    df = pd.DataFrame(all_comments)
    file_name = f'webtoon_{TARGET_WEBTOON_ID}_comments_final.xlsx'
    df.to_excel(file_name, index=False)
    print(f"\n🎉 총 {len(df)}개의 댓글 수집 완료! '{file_name}'으로 저장되었습니다.")
else:
    print("\n❌ 수집된 댓글이 없습니다. 최종 확인이 필요합니다.")