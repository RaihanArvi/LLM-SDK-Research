import json
from linkup.client import LinkupClient
from src.sdk_research.core.schemas import MetadataSchema, ExampleApp

"""

"""

class LinkupMetadataScraper:
    """
    """

    def __init__(self, linkup_api, include_list = None, exclude_list = None):
        """
        """
        self.client = LinkupClient(api_key=linkup_api)

        self.include_domains = include_list
        self.exclude_domains = exclude_list

    def _format_prompt(self, prompt, sdk_name, platform):
        if platform is not None:
            return prompt.format(sdk_name=sdk_name, platform=platform)
        else:
            return prompt.format(sdk_name=sdk_name)

    def _fetch_metadata(self, prompt) -> str:
        schema = MetadataSchema.model_json_schema()

        try:
            response = self.client.search(
                query=prompt,
                depth="standard",  # standard, deep
                output_type="structured",  # sourcedAnswer (natural languages with sources), searchResults (raw context)
                include_images=False,
                include_domains=self.include_domains,
                exclude_domains=self.exclude_domains,
                structured_output_schema=json.dumps(schema, indent=2),
                include_sources=True,
            )
            return response

        except Exception as e:
            return f"FETCH ERROR: {e}"

    def _parse_response(self, response) -> MetadataSchema:
        try:
            data = response.model_dump()["data"]

            flat_source_urls = list(set(data["source_urls"].values()))

            # Create MetadataSchema instance
            metadata = MetadataSchema(
                purpose=data["purpose"],
                developer=data["developer"],
                initial_release_date=data["initial_release_date"],
                key_features=data["key_features"],
                license_type=data["license_type"],
                platforms=data["platforms"],
                example_apps=data["example_apps"],
                source_urls=flat_source_urls
            )

            return metadata

        except Exception as e:
            exception_example_app = ExampleApp(
                name= f"FETCH ERROR: {e}",
                developer= f"FETCH ERROR: {e}",
                url= f"FETCH ERROR: {e}",
            )

            exception_response = MetadataSchema(
                purpose=f"FETCH ERROR: {e}",
                developer=f"FETCH ERROR: {e}",
                initial_release_date=f"FETCH ERROR: {e}",
                key_features = [f"FETCH ERROR: {e}"],
                license_type = f"FETCH ERROR: {e}",
                platforms = [f"FETCH ERROR: {e}"],
                example_apps = [exception_example_app],
                source_urls = ["www.FETCHERROR.com"],
            )

            return exception_response

    def fetch(self, prompt, sdk_name, platform) -> MetadataSchema:
        prompt_formatted = self._format_prompt(prompt, sdk_name, platform)  # format prompt.
        response = self._fetch_metadata(prompt_formatted)
        metadata = self._parse_response(response)

        return metadata
