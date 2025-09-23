from urllib.parse import urlparse
from typing import List, Tuple
import requests
from src.sdk_research.core.schemas import Release
"""
This module contains the GitHubCrawler class for crawling GitHub repositories to extract release notes.
Inputs:
- repo_url: str - The URL of the GitHub repository to crawl.
Outputs:
- SDKReleases - An object containing a list of Release objects with version, release date,
"""

class GitHubScraper:
    """
    A class to crawl GitHub repositories and extract release notes.
    """

    def __init__(self, crawler):
        """
        Initializes the GitHubCrawler with the repository URL.

        :param repo_url: The URL of the GitHub repository to crawl.
        """
        self.crawler = crawler
    
    def _extract_owner_repo(self, repo_url: str):
        parsed = urlparse(repo_url)  # splits into scheme, netloc, path, etc.
        path_parts = [p for p in parsed.path.split("/") if p]  # remove empty strings
        
        if len(path_parts) >= 2:
            owner, repo = path_parts[0], path_parts[1]
            return owner, repo
        else:
            raise ValueError(f"Invalid GitHub URL: {repo_url}")
    
    def _fetch_release_notes(self, owner: str, repo: str) -> List[Release]:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        r = requests.get(api_url)
        r.raise_for_status()

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
        if platform != None:
            return prompt.format(sdk_name=sdk_name, platform=platform)
        else:
            return prompt.format(sdk_name=sdk_name)
    
    def fetch(self, prompt, sdk_name, platform) -> Tuple[List[Release], str]:
        prompt_formatted = self._format_prompt(prompt, sdk_name, platform)

        top_repo_link = self.crawler.top_link(prompt_formatted)
        owner, repo = self._extract_owner_repo(top_repo_link)

        return self._fetch_release_notes(owner, repo), top_repo_link