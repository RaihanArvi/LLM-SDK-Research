from typing import Tuple
from src.sdk_research.crawler.linkup_crawler import LinkupCrawler
from src.sdk_research.scraper.github import GitHubScraper
from src.sdk_research.core.schemas import SDKReleaseNotesScraperResult

class LinkupGitHubReleaseNotesExtractor():

    def __init__(self, linkup_api):
        self.llm = None
        self.crawler = LinkupCrawler(api=linkup_api)
        self.scraper = GitHubScraper(self.crawler)

        # Description of the extractor
        self._name, self._version = "LinkupGitHubReleaseNotesExtractor", "0.1.0"
        self._description = "Linkup GitHub release notes extractor"

    def extract(self, prompt, sdk_name, platform=None) -> Tuple[SDKReleaseNotesScraperResult, str]:
        content, github_repo_link = self.scraper.fetch(prompt, sdk_name, platform)

        result = SDKReleaseNotesScraperResult(
            extractor_name=self._name,
            extractor_version=self._version,
            sdk_name=sdk_name,
            platform="NA" if platform == None else platform,
            truncated="No",  ##########
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
