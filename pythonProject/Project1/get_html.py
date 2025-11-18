# get_html.py (문제 페이지의 설계도를 가져오는 진단용 코드)

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

# 2. 쿠키 로그인
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

# 3. 문제가 발생하는 페이지로 이동
TARGET_WEBTOON_ID = '800770'
episode_num = 1
url = f"https://comic.naver.com/webtoon/detail?titleId={TARGET_WEBTOON_ID}&no={episode_num}"

print(f"--- {episode_num}화 페이지로 이동하여 페이지 소스를 저장합니다 ---")
driver.get(url)
time.sleep(5) # 페이지가 완전히 로드되도록 5초간 넉넉히 대기

# 4. 현재 페이지의 전체 HTML 소스 코드를 파일로 저장
try:
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    print("✅ 'page_source.html' 파일 저장이 완료되었습니다.")
    print("이 파일의 내용을 저에게 보내주세요.")
except Exception as e:
    print(f"❌ 파일 저장 중 오류 발생: {e}")
finally:
    driver.quit()