import requests
from src.sdk_research.crawler.base_crawler import BaseCrawler

class BraveCrawler(BaseCrawler):

    def __init__(self, brave_api):
        self.api = brave_api
        self.brave_tool = None
        self.name = "BraveCrawler"

        self.raw_results = ""
        self.link_results = []
        self.top_link_result = ""

    def _crawl_links_raw(self, prompt):
        
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={
                "X-Subscription-Token": self.api,
            },
            params={
                "q": prompt,
                "count": 5,
                "country": "us",
                "search_lang": "en",
            },
        ).json()

        self.raw_results = response
        return response
    
    def _crawl_links(self, prompt) -> list[str]:
        raw_response = self._crawl_links_raw(prompt)

        links = []
        if 'web' in raw_response and 'results' in raw_response['web']:
            for result in raw_response['web']['results']:
                url = result.get('url')
                if url:
                    links.append(url)
        
        return links

    def crawl(self, prompt):
        self.link_results = self._crawl_links(prompt)
        self.top_link_result = self.link_results[0]

        return self.top_link_result
