# main_crawler.py (더 강력한 선택자를 사용한 최종 버전)

import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

# 1. 크롬 드라이버 설정 (눈으로 보기 위해 헤드리스 해제)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

# 2. 쿠키를 이용해 로그인
print("저장된 쿠키를 불러와 로그인합니다...")
driver.get('https://www.naver.com')
time.sleep(1)
try:
    cookies = pickle.load(open("naver_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("✅ 쿠키 불러오기 성공!")
except FileNotFoundError:
    print("❌ 쿠키 파일을 찾을 수 없습니다.")
    driver.quit()
    exit()

# 3. 실제 크롤링 작업 수행
webtoon_info = {
    "title": "노블레스",
    "url": "https://comic.naver.com/webtoon/list?titleId=25455"
}
target_episodes = range(1, 4)  # 테스트를 위해 3개 회차만 수집
print(f"'{webtoon_info['title']}' 웹툰의 회차 정보를 수집합니다.")
driver.get(webtoon_info['url'])
time.sleep(2)

episodes = driver.find_elements(By.CSS_SELECTOR, 'a.EpisodeListList__link--DdClU')
target_urls = []
for episode in episodes:
    try:
        link = episode.get_attribute('href')
        if 'no=' in link:
            episode_num = int(link.split('no=')[1].split('&')[0])
            if episode_num in target_episodes:
                target_urls.append({'episode_num': episode_num, 'url': link})
    except Exception as e:
        continue
print(f"총 {len(target_urls)}개의 수집 대상 회차를 찾았습니다.")

all_comments = []
if target_urls:
    for target in sorted(target_urls, key=lambda x: x['episode_num']):
        print(f"--- {target['episode_num']}화 댓글 수집 시작 ---")
        driver.get(target['url'])
        time.sleep(0.3)

        # ★★★★★ 이 부분이 새로운 방식으로 변경되었습니다 ★★★★★

        # [변경점 1] '더보기' 버튼을 클래스 이름이 아닌, 눈에 보이는 '더보기'라는 텍스트로 찾습니다.
        while True:
            try:
                # '더보기'라는 텍스트를 포함하는 <span> 요소를 찾음 (더 강력한 방법)
                more_button = driver.find_element(By.XPATH, '//span[contains(text(), "더보기")]')
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)
            except NoSuchElementException:  # '더보기' 버튼이 더 이상 없으면
                print("'더보기' 버튼을 모두 클릭했습니다.")
                break
            except Exception as e:
                print(f"더보기 클릭 중 오류 발생: {e}")
                break

        # [변경점 2] 댓글을 찾을 때, 클래스 이름 전체가 아닌 '고정된 앞부분'만 보고 찾습니다.
        comment_selector = 'p[class^="CommentBox_comment_text"]'

        comments = driver.find_elements(By.CSS_SELECTOR, comment_selector)
        for comment in comments:
            all_comments.append({
                "webtoon": webtoon_info['title'],
                "episode": target['episode_num'],
                "comment": comment.text.strip()
            })
        print(f"✅ {target['episode_num']}화 댓글 {len(comments)}개 수집 완료")

driver.quit()

if all_comments:
    df = pd.DataFrame(all_comments)
    print(f"\n🎉 총 {len(df)}개의 댓글 수집 완료!")
    df.to_csv(f"{webtoon_info['title']}_comments_초반부_테스트.csv", index=False, encoding='utf-8-sig')
    print("CSV 파일 저장이 완료되었습니다.")
else:
    print("\n❌ 수집된 댓글이 없습니다. 로그인 또는 네트워크 상태를 확인해주세요.")