from typing import List, Tuple
from src.sdk_research.core.schemas import Release
from src.sdk_research.scraper.core.firecrawl_webpage_scraper import FirecrawlWebpageScraper
from src.sdk_research.crawler.serperdev_crawler import SerperDevCrawler
from src.sdk_research.parser.gemini_parser import GeminiParser


"""
Release notes scraper using Serper.dev + Firecrawl + Gemini (parsing). Scrape release notes from Websites/Documentation.

Constructor:
- API key.
- Schema (string).
- Domain filter list (include/exclude).
Outputs:
- List of Release objects.
"""


class SerperFirecrawlWebsiteReleaseNotesScraper:
    """
    A class to crawl GitHub repositories and extract release notes.
    """


    def __init__(self, serper_dev_api, firecrawl_api, gemini_api):
        """
        Constructor. Needs API for the services. The orders:
        1. Search for relevant docs link using Serper.dev.
        2. Given the docs link, parse the release notes.
        3. Parse the release notes using Gemini.
        """
        self.crawler = SerperDevCrawler(serper_dev_api)
        self.webpage_scraper = FirecrawlWebpageScraper(firecrawl_api)
        self.gemini_parser = GeminiParser(gemini_api)


    def _format_prompt(self, prompt, sdk_name, platform):
        if platform is not None:
            return prompt.format(sdk_name=sdk_name, platform=platform)
        else:
            return prompt.format(sdk_name=sdk_name)


    def _fetch_webpage(self, webpage_link) -> str:

        raw_webpage = self.webpage_scraper.scrape(webpage_link)

        return raw_webpage['data']['markdown']


    def _parse_release_notes(self, raw_webpage) -> List[Release]:
        return self.gemini_parser.parse(raw_webpage)


    def fetch(self, prompt, sdk_name, platform) -> Tuple[List[Release], str]:
        prompt_formatted = self._format_prompt(prompt, sdk_name, platform) # format prompt.

        self.crawler.crawl(prompt_formatted) # find links.
        top_docs_link = self.crawler.top_link_result # get the top link.
        raw_webpage = self._fetch_webpage(top_docs_link)

        return self._parse_release_notes(raw_webpage), top_docs_link
