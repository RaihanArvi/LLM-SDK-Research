from sdk_research.extractor.github_extractor import GitHubScraper
from src.sdk_research.core.schemas import SDKReleases
"""
This module contains functions to extract release notes from GitHub repositories given the SDK name.
"""

class LinkupReleaseNotesExtractor:
    """
    A class to extract release notes from GitHub repositories based on SDK names.
    """

    def __init__(self):
        self.llm = None
        self.crawler = None

        # Description of the extractor
        self.name, self.version = "LinkupReleaseNotesExtractor", "0.1.0"

    def _extract_sdk_releases(self, sdk_name: str) -> SDKReleases:
        """
        Internal method to extract SDK releases using the GitHub crawler.

        :param sdk_name: The name of the SDK whose release notes are to be extracted.
        :return: An SDKReleases object containing the extracted release notes.
        """
        relevant_links = None

        releases = GitHubScraper().fetch(top_url)
        return SDKReleases(content=releases)

    def extract(sdk_name: str) -> SDKScrapperResult:
        """
        Extracts release notes from the GitHub repository corresponding to the given SDK name.

        :param sdk_name: The name of the SDK whose release notes are to be extracted.
        :return: An SDKReleases object containing the extracted release notes.
        """
        releases = self._extract_sdk_releases(sdk_name)
        return SDKScrapperResult(
            name=self.name,
            version=self.version,
            releases=releases
        )

    # Getters

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def version(self) -> str:
        return self._version
    
    @property
    def crawler(self) -> str:
        return self.crawler
