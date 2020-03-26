from urllib import request
from bs4 import BeautifulSoup
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


class blind_html():
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
    s = blind_html(url)
    s.get_thread()