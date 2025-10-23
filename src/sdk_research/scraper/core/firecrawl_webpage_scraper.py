import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

class RetryableHTTPError(requests.exceptions.RequestException):
    """Raised for retryable HTTP status codes (429, 5xx)."""
    pass

class FirecrawlWebpageScraper():

    def __init__(self, firecrawl_api):
        self.firecrawl_api = firecrawl_api


    @retry(
        retry=retry_if_exception_type((
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            RetryableHTTPError
        )),
        stop=stop_after_attempt(7),
        wait=wait_exponential(multiplier=1, min=1, max=30)
    )
    def _scrape(self, link):
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

        if response.status_code in [429, 500, 502, 503, 504]:
            raise RetryableHTTPError(f"API returned status code {response.status_code}")

        response.raise_for_status()
        return response.json()


    def scrape(self, link):
        try:
            return self._scrape(link)
        except Exception as e:
            placeholder_dict = {
                "success": True,
                "data": {
                    "markdown": "SCRAPING ERROR",
                    "summary": "",
                    "links": [],
                    "html": ""
                }
            }

            return placeholder_dict

