from urllib import request
from bs4 import BeautifulSoup
import re
import os


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_article_urls():
    url_str = 'https://www.teamblind.com'
    with request.urlopen(url_str) as url:
        s = url.read()
    soup = BeautifulSoup(s)
    articles_list = soup.find('div', {'class': 'lst_wrap'})
    articles_list = articles_list.find_all('li', {'class': 'word-break'})
    article_urls = []
    for article in articles_list:
        link_ext = article.find('a', href=True)
        if link_ext is not None:
            article_urls.append(url_str + link_ext['href'])
    return article_urls


class blind_thread():
    def __init__(self, url):
        with request.urlopen(url) as url:
            s = url.read()
        self.soup = BeautifulSoup(s)

    def get_thread(self):
        # get main thread text
        thread = self.soup.p.get_text(' ')
        company = self.soup.find('div', {'class': 'writer'}).a.get_text()
        return thread, company


if __name__ == '__main__':
    url = 'https://www.teamblind.com/post/Amazon-phone-screening-ByCM6MB6'
    url = 'https://www.teamblind.com/post/Who-needs-a-co-founder-XyWjhctu'
    s = blind_thread(url)
    s.get_thread()
    get_article_urls()