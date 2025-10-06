from urllib.parse import urlparse
from typing import List, Tuple
import requests
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

    def _fetch_release_notes(self, owner: str, repo: str) -> List[Release]:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"

        try:
            r = requests.get(api_url)
            r.raise_for_status()
        except Exception as e:
            release = Release(
                version="v9.9.9.9",
                release_date=f"GIT SCRAP ERROR: {e}",
                notes=f"GIT SCRAP ERROR: {e}",
                source_url=f"GIT SCRAP ERROR: {e}"
            )
            return [release]

        releases = []
        for rel in r.json():
            release = Release(
                version=rel["tag_name"],
                release_date=rel["published_at"][:10],
                notes=(rel["body"] or "")[:1000],
                source_url=rel.get("html_url")
            )
            releases.append(release)

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