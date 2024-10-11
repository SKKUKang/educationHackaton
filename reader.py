import requests
from bs4 import BeautifulSoup

# URL to access (replace with the actual article URL)
url = "https://n.news.naver.com/article/001/0014978628?type=journalists"

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
