from src.sdk_research.scraper.linkup_metadata_scraper import LinkupMetadataScraper
from src.sdk_research.core.schemas import SDKMetadataScraperResult

class MetadataExtractor:
    """

    """
    def __init__(self, linkup_api, include_list = None, exclude_list = None):
        self.scraper = LinkupMetadataScraper(linkup_api, include_list, exclude_list)

        # Description of the extractor
        self._name, self._version = "LinkupMetadataExtractor", "0.1.0"
        self._description = "LinkupMetadataExtractor"

    def extract(self, prompt, sdk_name):
        metadata = self.scraper.fetch(prompt, sdk_name, platform=None)

        extractor_result = SDKMetadataScraperResult(
            extractor_name=self._name,
            extractor_version=self._version,
            sdk_name=sdk_name,
            metadata=metadata,
        )

        return extractor_result

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description
