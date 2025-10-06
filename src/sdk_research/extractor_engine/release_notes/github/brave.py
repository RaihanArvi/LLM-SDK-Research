from typing import Tuple
from src.sdk_research.crawler.brave import BraveCrawler
from src.sdk_research.scraper.github import GitHubScraper
from src.sdk_research.core.schemas import SDKReleaseNotesScraperResult

class BraveGitHubReleaseNotesExtractor():

    def __init__(self, brave_api):
        self.llm = None
        self.crawler = BraveCrawler(brave_api=brave_api)
        self.scraper = GitHubScraper(self.crawler)

        # Description of the extractor
        self._name, self._version = "BraveGitHubReleaseNotesExtractor", "0.1.0"
        self._description = "Brave GitHub release notes extractor"

    def extract(self, prompt, sdk_name, platform = None) -> Tuple[SDKReleaseNotesScraperResult, str]:
        content, github_repo_link = self.scraper.fetch(prompt, sdk_name, platform)

        result = SDKReleaseNotesScraperResult(
            extractor_name=self._name,
            extractor_version=self._version,
            sdk_name=sdk_name,
            platform="NA" if platform == None else platform,
            truncated="No", ##########
            releases=content,
        )

        return result, github_repo_link

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description
