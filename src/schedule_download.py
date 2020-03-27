import datetime
import time

import schedule

from extract import download_threads, get_article_urls


def download():
    urls = get_article_urls()
    download_threads(urls)


def job():
    try:
        print('Job Started')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        download()
        print('Job Done')
    except:
        print('Timed Out.')


if __name__ == "__main__":
    job()
    schedule.every(10).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
