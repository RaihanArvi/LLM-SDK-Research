from src.sdk_research.scraper.serper_firecrawl_docs_release_notes import SerperFirecrawlWebsiteReleaseNotesScraper
from src.sdk_research.core.schemas import SDKReleaseNotesScraperResult

"""
Release Notes Extractor Engine.
Extract release notes from SDK's website/documentation using Serper + Firecrawl + Gemini.
"""

class SerperFirecrawlWebsiteReleaseNotesExtractor:

    def __init__(self, serper_dev_api, firecrawl_api, gemini_api):

        self.scraper = SerperFirecrawlWebsiteReleaseNotesScraper(serper_dev_api, firecrawl_api, gemini_api)

        # Description of the extractor
        self._name, self._version = "SerperFirecrawlWebsiteReleaseNotesExtractor", "0.1.0"
        self._description = "Serper + Firecrawl + Gemini documentation/website release notes extractor."

    def extract(self, prompt, sdk_name, platform=None) -> SDKReleaseNotesScraperResult:
        releases = self.scraper.fetch(prompt, sdk_name, platform)

        result = SDKReleaseNotesScraperResult(
            extractor_name=self._name,
            extractor_version=self._version,
            sdk_name=sdk_name,
            platform="NA" if platform is None else platform,
            truncated="No",
            releases=releases,
        )

        return result

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description

