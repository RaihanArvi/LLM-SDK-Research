import requests

class BraveCrawler():

    def __init__(self, brave_api):
        self.api = brave_api
        self.brave_tool = None
        self.name = "BraveCrawler"

    def crawl_links_raw(self, prompt):
        
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

        return response
    
    def crawl_links(self, prompt) -> list[str]:
        raw_response = self.crawl_links_raw(prompt)

        links = []
        if 'web' in raw_response and 'results' in raw_response['web']:
            for result in raw_response['web']['results']:
                url = result.get('url')
                if url:
                    links.append(url)
        
        return links
    
    def top_link(self, prompt) -> str:
        return self.crawl_links(prompt)[0]
        





