import requests
from bs4 import BeautifulSoup
import time

def get_posts_from_page(soup):
    posts = []
    for post in soup.find_all('div', class_='titlelink box'):
        title = post.find('a').get_text(strip=True)
        link = post.find('a')['href']
        posts.append((title, link))
    return posts

def get_next_page_url(soup):
    next_page = soup.find('a', string='下一页')
    if next_page:
        return next_page['href']
    return None

def crawl_hupu_forum(start_url):
    url = start_url
    all_posts = []

    while url:
        print(f'Crawling page: {url}')
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        posts = get_posts_from_page(soup)
        if not posts:
            print("No posts found on this page.")
        all_posts.extend(posts)

        next_page_url = get_next_page_url(soup)
        if not next_page_url:
            print("No next page found.")
            break
        url = next_page_url

        time.sleep(1)  # 避免请求过于频繁

    return all_posts

if __name__ == "__main__":
    start_url = 'https://bbs.hupu.com/73-postdate'
    posts = crawl_hupu_forum(start_url)
    for title, link in posts:
        print(f'Title: {title}, Link: {link}')