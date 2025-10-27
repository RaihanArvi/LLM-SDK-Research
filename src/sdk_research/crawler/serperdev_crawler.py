from src.sdk_research.crawler.base_crawler import BaseCrawler
import http.client
import json

"""
Crawler using serper.dev.
"""

class SerperDevCrawler(BaseCrawler):

    def __init__(self, serper_dev_api):
        self.api = serper_dev_api

        self.raw_results = ""
        self.link_results = []
        self.top_link_result = ""


    def _crawl_links_raw(self, query):
        """
        Send request to serper.dev.
        :return: multiline raw json response.
        :except:
        """

        try:
            conn = http.client.HTTPSConnection("google.serper.dev")
            payload = json.dumps({
                "q": f"{query}",
            })
            headers = {
                'X-API-KEY': f'{self.api}',
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            data = res.read()
            raw_json_str = data.decode("utf-8")
            raw_json = json.loads(raw_json_str)

            self.raw_results = raw_json_str

            return raw_json

        except Exception as e:
            # Error placeholder
            error_dict = {
                "organic": [
                    {
                        "title": f"ERROR: {e}",
                        "link": f"ERROR: {e}",
                    }
                ]
            }

            return error_dict


    def _crawl_links(self, prompt) -> list[str]:
        raw_response = self._crawl_links_raw(prompt)

        links = []
        for result in raw_response['organic']:
            links.append(result['link'])

        return links


    def crawl(self, prompt):
        self.link_results = self._crawl_links(prompt)
        self.top_link_result = self.link_results[0]

        return self.top_link_result

