import csv
import logging
import time
import os
from urllib.parse import urljoin, urlparse, urlunparse, urldefrag

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.session = requests.Session()

    def normalize_url(self, url):
        url_parts = urlparse(url)
        normalized_url = urlunparse(
            (url_parts.scheme, url_parts.netloc, url_parts.path, "", "", ""))
        normalized_url, _ = urldefrag(normalized_url)
        return normalized_url

    def download_url(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = self.session.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield self.normalize_url(path)

    def extract_text(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator='\n')

    def add_url_to_visit(self, url):
        url = self.normalize_url(url)
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        text = self.extract_text(html)
        for linked_url in self.get_linked_urls(url, html):
            self.add_url_to_visit(linked_url)

        # Save visited URL and text content to a unique .txt file
        filename = url.replace('http://', '').replace('https://', '').replace('/', '_').replace('?', '!').replace('=',
                                                                                                                  '-')

        if not os.path.isfile(f'data/{filename}.txt'):
            with open(f'data/{filename}.txt', 'w', encoding='utf-8') as file:
                file.write(text)
        else:
            file_number = 1
            while os.path.isfile(f'data/{filename}_{file_number}.txt'):
                file_number += 1
            with open(f'data/{filename}_{file_number}.txt', 'w', encoding='utf-8') as file:
                file.write(text)

        # Introduce a delay between requests
        time.sleep(1)

    def run(self):
        os.makedirs('data', exist_ok=True)
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)


if __name__ == '__main__':
    Crawler(urls=['https://www.imdb.com']).run()
    print(" Crawling completed! ")
