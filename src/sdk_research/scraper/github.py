import time
from urllib.parse import urlparse
from typing import List, Tuple
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.sdk_research.core.schemas import Release


"""
This module contains the GitHubCrawler class for crawling GitHub repositories to extract release notes.

Given prompt format, SDK name, and platform (optional), it will:
    1. Crawl to find relevant GitHub links, pick the top one. 
    2. Extract release notes from the GitHub repository.
    
Inputs:
- Crawler object.

Outputs:
- List of Release objects.
"""


class GitHubScraper:
    """
    A class to crawl GitHub repositories and extract release notes.
    """


    def __init__(self, crawler):
        """
        Initializes the GitHubCrawler.
        """
        self.crawler = crawler


    def _extract_owner_repo(self, repo_url: str):
        parsed = urlparse(repo_url)  # splits into schema, netloc, path, etc.
        path_parts = [p for p in parsed.path.split("/") if p]  # remove empty strings
        
        if len(path_parts) >= 2:
            owner, repo = path_parts[0], path_parts[1]
            return owner, repo
        else:
            return "", "" # If the link supplied is not a GitHub link.


    @retry(
        reraise=True,
        stop=stop_after_attempt(5),          # retry up to 5 times
        wait=wait_exponential(multiplier=1, min=2, max=10),  # backoff: 2s, 4s, 8s, ...
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def _fetch_page(self, url: str, headers: dict) -> requests.Response:
        """Fetch a single page of GitHub releases with retry logic."""
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r

    def _fetch_release_notes(self, owner: str, repo: str) -> List[Release]:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=100"
        headers = {
            "Accept": "application/vnd.github+json",
        }

        # Optional: include token to avoid rate limits
        # token = os.getenv("GITHUB_TOKEN")
        # if token:
        #     headers["Authorization"] = f"Bearer {token}"

        releases = []
        url = api_url

        try:
            while url:
                r = self._fetch_page(url, headers)
                data = r.json()

                for rel in data:
                    release = Release(
                        version=rel.get("tag_name", "N/A"),
                        release_date=(rel.get("published_at") or "N/A")[:10],
                        notes=(rel.get("body") or "")[:1000],
                        source_url=rel.get("html_url", "")
                    )
                    releases.append(release)

                # Parse pagination links from the headers
                link = r.headers.get("Link", "")
                next_url = None
                if link:
                    parts = link.split(",")
                    for part in parts:
                        if 'rel="next"' in part:
                            next_url = part[part.find("<") + 1: part.find(">")]
                            break
                url = next_url
                time.sleep(0.25)

        except Exception as e:
            release = Release(
                version="v9.9.9.9",
                release_date=f"GIT SCRAP ERROR: {e}",
                notes=f"GIT SCRAP ERROR: {e}",
                source_url=f"GIT SCRAP ERROR: {e}"
            )
            return [release]

        return releases

    
    def _format_prompt(self, prompt, sdk_name, platform):
        if platform is not None:
            return prompt.format(sdk_name=sdk_name, platform=platform)
        else:
            return prompt.format(sdk_name=sdk_name)


    def fetch(self, prompt, sdk_name, platform) -> Tuple[List[Release], str]:
        prompt_formatted = self._format_prompt(prompt, sdk_name, platform) # format prompt.

        self.crawler.crawl(prompt_formatted) # find links.
        top_repo_link = self.crawler.top_link_result # get the top link.
        owner, repo = self._extract_owner_repo(top_repo_link)

        return self._fetch_release_notes(owner, repo), top_repo_link
