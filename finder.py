import json
import requests
from bs4 import BeautifulSoup


def get_press_code(press_name):
    # press_links.json 파일 읽기
    with open('press_links.json', 'r', encoding='utf-8') as file:
        press_links = json.load(file)
    
    # 언론사 이름으로 숫자 찾기
    for code, name in press_links.items():
        if name == press_name:
            return code
    
    return None

def find_journalist_in_json(press_code, journalist_name):
    # {code}_journalists.json 파일 읽기
    try:
        with open(f'journalists\{press_code}_journalists.json', 'r', encoding='utf-8') as file:
            journalist_data = json.load(file)
        
        journalists = journalist_data.get(str(press_code), {})
        if journalist_name in journalists:
            url_code = journalists[journalist_name]
            journalist_url = f"https://media.naver.com/journalist/{press_code}/{url_code}"
            return journalist_url
        else:
            return None
    except FileNotFoundError:
        print(f"{press_code}_journalists.json 파일을 찾을 수 없습니다.")
        return None

def get_article_text(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the article element
        article = soup.find('article')
        
        # Check if the article exists
        if article:
            # Extract all text from the article
            article_text = article.get_text(separator='\n', strip=True)
            print("기사 본문:")
            print(article_text)
        else:
            print("Article not found.")
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)




# 테스트
press_name = input("언론사 이름을 입력하세요: ")
code = get_press_code(press_name)

if code:
    print("언론사가 정상적으로 입력되었습니다")
    journalist_name = input("기자 이름을 입력하세요: ")
    
    journalist_url = find_journalist_in_json(code, journalist_name)
    if journalist_url:
        print(f"{journalist_name} 기자를 찾았습니다: {journalist_url}")
    else:
        print(f"{journalist_name} 기자를 찾을 수 없습니다.")
else:
    print(f"{press_name}을(를) 찾을 수 없습니다.")


# URL 설정
url = journalist_url

# HTTP 요청을 통해 HTML 소스 가져오기
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 0. 소속 (Organization)
organization = soup.select_one('span.media_reporter_basic_press_txt').get_text()

# 1. 기자 이름 (Journalist Name)
journalist_name = soup.select_one('h2.media_reporter_basic_name').get_text()

# 2. 구독자 수 (Subscribers)
subscriber_count = soup.find('em', class_='media_reporter_popularity_subscribenum _journalist_subscribe_count _txt').get_text()

# 3. 한달간 기사 수 (Articles in the last month)
articles_count = soup.select_one('li.media_reporter_summary_item em').get_text() + '건'

# 4. 주 섹션 (Main Section)
main_section = soup.select('li.media_reporter_summary_item em')[1].get_text()

# 5. 성별 통계 (Gender Statistics)
text_elements = soup.select('g.bb-target-male')
for text in text_elements:
        print(text.get_text())

# 6. 구독자 나이 통계 (Subscriber Age Statistics)
age_stats = {
    '10대': soup.select_one('div.group:nth-child(1) span.percent').get_text(),
    '20대': soup.select_one('div.group:nth-child(2) span.percent').get_text(),
    '30대': soup.select_one('div.group:nth-child(3) span.percent').get_text(),
    '40대': soup.select_one('div.group:nth-child(4) span.percent').get_text(),
    '50대': soup.select_one('div.group:nth-child(5) span.percent').get_text(),
    '60대 이상': soup.select_one('div.group:nth-child(6) span.percent').get_text()
}

# 7. 최근 기사들의 제목과 URL (Recent Articles Titles and URLs)
recent_articles = []
articles = soup.select('div._latest_writings article a')
for article in articles:
    title = article.get_text()
    url = article['href']
    recent_articles.append((title, url))

# Output parsed data
print(f"0. 소속: {organization}")
print(f"1. 기자 이름: {journalist_name}")
print(f"2. 구독자 수: 아직 안됨")
print(f"3. 한달간 기사 수: {articles_count}")
print(f"4. 주 섹션: {main_section}")
print(f"5. 성별 통계: 아직 안됨")
print(f"6. 구독자 나이 통계: {age_stats}")
print("7. 최근 기사들:")

news_items = soup.find_all('a', class_='press_edit_news_link')

count=0
    # Extract title and URL for each news item


titleURL = []
for item in news_items:
    title = item.find('span', class_='press_edit_news_title').text
    url = item['href']
    print(f'제목: {title}')
    print(f'url: "{url}"')
    print()  # Print a blank line between items
    #title과 url을 mapping 하여 저장
    titleURL.append((title, url))

for i in range(len(titleURL)):
    get_article_text(titleURL[i][1])
    print()
    print()
      # Print a blank line between items











