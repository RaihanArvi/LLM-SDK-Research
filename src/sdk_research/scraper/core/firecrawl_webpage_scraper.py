import requests

class FirecrawlWebpageScraper():

    def __init__(self, firecrawl_api):
        self.firecrawl_api = firecrawl_api


    def scrape(self, link):
        url = "https://api.firecrawl.dev/v2/scrape"

        payload = {
            "url": link,
            "onlyMainContent": False,
            "maxAge": 172800000,
            "parsers": [],
            "formats": [
                "markdown",
                "summary",
                "links",
                "html"
            ]
        }

        headers = {
            "Authorization": f"Bearer {self.firecrawl_api}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        json = response.json()

        return json

