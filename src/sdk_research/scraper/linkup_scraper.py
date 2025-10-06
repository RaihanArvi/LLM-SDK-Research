import json
from typing import List
from linkup.client import LinkupClient
from src.sdk_research.core.schemas import Release


"""
Release notes scraper using Linkup. Scrape release notes from Websites/Documentation.

Constructor:
- API key.
- Schema (string).
- Domain filter list (include/exclude).
Outputs:
- List of Release objects.
"""


class LinkupWebsiteReleaseNotesScraper:
    """
    A class to crawl GitHub repositories and extract release notes.
    """

    def __init__(self, linkup_api, output_json_schema, include_list = None, exclude_list = None):
        """
        """
        self.client = LinkupClient(api_key=linkup_api)

        self.include_domains = include_list
        self.exclude_domains = exclude_list

        self.schema = output_json_schema

    def _format_prompt(self, prompt, sdk_name, platform):
        if platform is not None:
            return prompt.format(sdk_name=sdk_name, platform=platform)
        else:
            return prompt.format(sdk_name=sdk_name)

    def _fetch_release_notes(self, prompt) -> str:

        try:
            response = self.client.search(
                query=prompt,
                depth="standard",  # standard, deep
                output_type="structured",
                # sourcedAnswer (natural languages with sources), searchResults (raw context)
                include_images=False,
                include_domains=self.include_domains,
                exclude_domains=self.exclude_domains,
                structured_output_schema=self.schema,
                include_sources=True,
            )
        except Exception as e:
            exception_response = """{
  "data": {
    "versions": [
      {
        "version_number": f"FETCH ERROR {e}",
        "release_date": f"FETCH ERROR {e}",
        "summary_notes": f"FETCH ERROR FOR {prompt}: {e}"
      },
  },
  "sources": [
    {
      "content": "",
      "name": "",
      "type": "",
      "url": ""
    }
  ]
}"""
            exception_response.format(e = e, prompt = prompt)
            return exception_response

        return response

    def _parse_response(self, response) -> List[Release]:
        try:
            parsed = json.loads(response)

            # Take the first source URL
            source_url = parsed["sources"][0]["url"]

            releases = []
            for v in parsed["data"]["versions"]:
                releases.append(
                    Release(
                        version=v["version_number"],
                        release_date=v["release_date"],
                        notes=v["summary_notes"],
                        source_url=source_url,
                    )
                )

            return releases # this is a list of Releases.

        except Exception as e:
            exception_response = [Release(version="PARSE ERROR",
                                          release_date="PARSE ERROR",
                                          notes=f"PARSE ERROR FOR {response}: {e}",
                                          source_url="")]
            return exception_response

    def fetch(self, prompt, sdk_name, platform) -> List[Release]:
        prompt_formatted = self._format_prompt(prompt, sdk_name, platform)  # format prompt.

        response = self._fetch_release_notes(prompt_formatted)
        release_notes = self._parse_response(response)

        return release_notes
