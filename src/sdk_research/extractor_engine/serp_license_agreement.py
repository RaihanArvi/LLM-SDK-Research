from src.sdk_research.crawler.serperdev_crawler import SerperDevCrawler
from src.sdk_research.core.prompts import licence_agreement_query_general

"""
Extractor for Licence Agreement. Based on Google Serper.
"""

class LicenseAgreementExtractor:

    def __init__(self, serper_api):
        self.crawler = SerperDevCrawler(serper_api)

        # Description of the extractor
        self._name, self._version = "LicenseAgreementExtractor", "0.1.0"
        self._description = "License Agreement Extractor using Google Serper."


    def _format_prompt(self, prompt, sdk_name, platform):
        if platform is not None:
            return prompt.format(sdk_name=sdk_name, platform=platform)
        else:
            return prompt.format(sdk_name=sdk_name)


    def extract(self, sdk_name, platform=None):
        query = self._format_prompt(licence_agreement_query_general, sdk_name, platform)
        top_link = self.crawler.crawl(query)

        return self.crawler.link_results # return a list of str instead.


    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description
