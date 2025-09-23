import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.sdk_research.core.schemas import MetadataStructuredOutput
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool

class MetadataExtractor():
    """

    """
    def __init__(self, llm, output_format = None):
        self.llm = llm
        self.output_format = output_format

        # Description of the extractor
        self._name, self._version = "MetadataExtractor", "0.1.0"
        self._description = "MetadataExtractor"

    def _parse(self, response):
        print(response.content)
        response_json = json.loads(response.content)
        print(response_json)
        return MetadataStructuredOutput(**response_json)

    def extract(self, prompt, sdk_name, is_structured_output = False):

        if is_structured_output:
            message_send = [
                HumanMessage(content=f"{prompt.format(SDK_NAME=sdk_name)}")
            ]
            llm_so = self.llm.with_structured_output(MetadataStructuredOutput)

            return llm_so.invoke(message_send)
        else:
            message_send = [
                SystemMessage(content=f"{self.output_format}"),
                HumanMessage(content=prompt.format(SDK_NAME=sdk_name))
            ]

            response = self.llm.invoke(message_send)
            parsed_response = self._parse(response)

            return parsed_response

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description
