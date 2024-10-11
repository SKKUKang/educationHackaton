import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def get_remaining_press_codes(start=5):
    # press_links.json 파일 읽기
    with open('press_links.json', 'r', encoding='utf-8') as file:
        press_links = json.load(file)
    
    # 상위 start개 항목을 제외한 나머지 언론사 코드와 이름 가져오기
    remaining_press_codes = list(press_links.items())[start:]
    return remaining_press_codes

def clean_journalist_name(name):
    # 불필요한 텍스트 제거 및 첫 번째 띄어쓰기 전까지만 저장
    name = name.strip().replace('\n', '').replace('구독', '').replace('TALK', '').strip()
    return name.split()[0]

def collect_journalists(press_code):
    url = f"https://media.naver.com/journalists/{press_code}/?order=name"
    
    # Headless Chrome 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 창을 띄우지 않음
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Selenium으로 브라우저 열기
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)  # 페이지 로드 대기

    # 페이지 끝까지 스크롤링 (무한 스크롤 시뮬레이션)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 스크롤을 페이지 끝까지 내리기
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # 스크롤 후 로딩 대기
        
        # 새로운 높이 측정
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # 더 이상 스크롤할 수 없으면 종료
        last_height = new_height

    # 스크롤 후 HTML 소스 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # journalist_list_content_title 클래스를 가진 요소 찾기
    journalists = soup.find_all(class_='journalist_list_content_title')

    journalist_data = {}
    for journalist in journalists:
        name = clean_journalist_name(journalist.text)
        url = journalist.find('a')['href']
        url_code = url.split('/')[-1]
        journalist_data[name] = url_code

    # 브라우저 닫기
    driver.quit()

    return journalist_data

# 상위 5개 항목을 제외한 나머지 언론사 코드와 이름 가져오기
remaining_press_codes = get_remaining_press_codes(5)

for code, press_name in remaining_press_codes:
    print(f"{press_name}의 코드: {code}")
    journalist_data = collect_journalists(code)
    
    # JSON 파일로 저장
    with open(f'{code}_journalists.json', 'w', encoding='utf-8') as file:
        json.dump({code: journalist_data}, file, ensure_ascii=False, indent=4)
    
    print(f"{press_name}의 기자 목록이 {code}_journalists.json 파일에 저장되었습니다.")