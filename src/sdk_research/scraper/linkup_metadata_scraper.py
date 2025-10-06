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
            data = response.data

            source_urls = []
            for source in response.sources:
                source_urls.append(source.url)

            # Create MetadataSchema instance
            metadata = MetadataSchema(
                purpose=data["purpose"],
                developer=data["developer"],
                initial_release_date=data["initial_release_date"],
                key_features=data["key_features"],
                documentation_url=data["documentation_url"],
                license_type=data["license_type"],
                platforms=data["platforms"],
                example_apps=data["example_apps"],
                source_urls=source_urls
            )

            return metadata

        except Exception as e:
            exception_example_app = ExampleApp(
                name= f"PARSE ERROR: {e}",
                developer= f"PARSE ERROR: {e}",
                url= f"PARSE ERROR: {e}",
            )

            exception_response = MetadataSchema(
                purpose=f"PARSE ERROR: {e}",
                developer=f"PARSE ERROR: {e}",
                initial_release_date=f"PARSE ERROR: {e}",
                key_features = [f"PARSE ERROR: {e}"],
                documentation_url = f"PARSE ERROR: {e}",
                license_type = f"PARSE ERROR: {e}",
                platforms = [f"PARSE ERROR: {e}"],
                example_apps = [exception_example_app],
                source_urls = ["www.PARSEERROR.com"],
            )

            return exception_response

    def fetch(self, prompt, sdk_name, platform) -> MetadataSchema:
        prompt_formatted = self._format_prompt(prompt, sdk_name, platform)  # format prompt.
        response = self._fetch_metadata(prompt_formatted)
        metadata = self._parse_response(response)

        return metadata
