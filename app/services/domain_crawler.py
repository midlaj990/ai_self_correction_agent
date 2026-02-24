import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


class DomainCrawler:

    def __init__(self, max_pages=30):
        self.max_pages = max_pages
        self.visited = set()

    def crawl(self, start_url):
        results = []
        self._crawl_recursive(start_url, start_url, results)
        return results

    def _crawl_recursive(self, base_url, current_url, results):
        if len(self.visited) >= self.max_pages:
            return

        if current_url in self.visited:
            return

        self.visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=5)
            soup = BeautifulSoup(response.text, "lxml")

            text = soup.get_text(separator="\n")
            results.append(text)

            for link in soup.find_all("a", href=True):
                next_url = urljoin(base_url, link["href"])
                if urlparse(next_url).netloc == urlparse(base_url).netloc:
                    self._crawl_recursive(base_url, next_url, results)

            time.sleep(0.5)

        except Exception:
            pass
