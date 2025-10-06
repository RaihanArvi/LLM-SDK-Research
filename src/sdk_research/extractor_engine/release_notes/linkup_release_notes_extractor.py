from src.sdk_research.scraper.linkup_scraper import LinkupWebsiteReleaseNotesScraper
from src.sdk_research.core.schemas import linkup_schema, SDKReleaseNotesScraperResult

"""
Extract release notes from SDK's website/documentation using Linkup.
"""

class LinkupWebsiteReleaseNotesExtractor:

    def __init__(self, linkup_api, include_list = None, exclude_list = None):
        self.scraper = LinkupWebsiteReleaseNotesScraper(linkup_api, linkup_schema,
                                                        include_list, exclude_list)

        # Description of the extractor
        self._name, self._version = "LinkupWebsiteReleaseNotesExtractor", "0.1.0"
        self._description = "Linkup documentation/website release notes extractor."

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
