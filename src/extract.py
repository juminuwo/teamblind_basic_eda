import os
import re
from urllib import request

import pandas as pd
from bs4 import BeautifulSoup


def add_thread(contents, companies, url):
    s = blind_thread(url)
    content, company = s.get_thread()
    print('-----')
    print('Thread Content: {}'.format(content))
    print('Company: {}'.format(company))
    contents.append(content)
    companies.append(company)
    return content, company, url


def download_threads(urls):
    contents = []
    companies = []
    for url in urls:
        if os.path.isfile('threads.csv'):
            df = pd.read_csv('threads.csv')
        else:
            df = []
        if isinstance(df, pd.DataFrame):
            if url not in df.iloc[:, 2]:
                content, company, url = add_thread(contents, companies, url)
        else:
            content, company, url = add_thread(contents, companies, url)
        df = pd.DataFrame({
            'content': [content],
            'company': [company],
            'url': [url]
        })
        df.to_csv('threads.csv', mode='a', header=False, index=False)
    return df


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_article_urls():
    url_str = 'https://www.teamblind.com'
    with request.urlopen(url_str) as url:
        s = url.read()
    soup = BeautifulSoup(s, features='html.parser')
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
        self.regex = re.compile('[^a-zA-Z]')

    def get_thread(self):
        # get main thread text
        #thread = self.soup.p.get_text(' ')
        #company = self.soup.find('div', {'class': 'writer'}).a.get_text()
        thread = self.soup.find('div', {
            'class': 'detail word-break'
        }).p.get_text(' ')
        company = self.soup.find('div', {'class': 'writer'}).span.text[:-1]
        company = self.regex.sub('', company)
        return thread, company


if __name__ == '__main__':
    # url = 'https://www.teamblind.com/post/Amazon-phone-screening-ByCM6MB6'
    # url = 'https://www.teamblind.com/post/Who-needs-a-co-founder-XyWjhctu'
    # url = 'https://www.teamblind.com/post/how-is-sunnyvale-ca-is-it-bad-relatively-compared-to-sf-30VHQPAR'
    # url = 'https://www.teamblind.com/post/TripActions-Laidoff-350-People-QdmaW3Z8'
    # s = blind_thread(url)
    # s.get_thread()

    urls = get_article_urls()
    download_threads(urls)
