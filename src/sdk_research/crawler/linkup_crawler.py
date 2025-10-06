from src.sdk_research.crawler.base_crawler import BaseCrawler
from linkup import LinkupClient
"""
Crawler using Linkup.
"""

class LinkupCrawler(BaseCrawler):

    def __init__(self, api, include_list = None, exclude_list = None):
        self.api = api
        self.client = LinkupClient(api_key=self.api)

        self.include_domains = include_list
        self.exclude_domains = exclude_list

        self.raw_results = ""
        self.link_results = []
        self.top_link_result = ""

    def _crawl_links_raw(self, prompt):

        response = self.client.search(
            query=prompt,
            depth="standard",  # standard, deep
            output_type="searchResults",  # sourcedAnswer (natural languages with sources), searchResults (raw context)
            include_images=False,
            include_domains=self.include_domains,
            exclude_domains=self.exclude_domains,
        )

        return response

    def _crawl_links(self, prompt) -> list[str]:
        raw_response = self._crawl_links_raw(prompt)

        links = []
        for result in raw_response.results:
            links.append(result.url)

        return links

    def crawl(self, prompt):
        self.link_results = self._crawl_links(prompt)
        self.top_link_result = self.link_results[0]

        return self.top_link_result
