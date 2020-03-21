from retrying import retry
import requests
from loguru import logger
import time

class BaseCrawler(object):
    urls = []
    
    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)
    def fetch(self, url, **kwargs):
        try:
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                return response.text
        except requests.ConnectionError:
            return
    
    @logger.catch
    def crawl(self):
        """
        crawl main method
        """
        for url in self.urls:
            logger.info(f'fetching {url}')
            time.sleep(1) #some sites may have protection(e.g. kuaidaili)
            html = self.fetch(url)
            for proxy in self.parse(html):
                logger.info(f'fetched proxy {proxy.string()} from {url}')
                yield proxy
