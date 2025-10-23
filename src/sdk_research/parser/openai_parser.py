from src.sdk_research.core.prompts import release_notes_parser_instructions
from src.sdk_research.core.schemas import Releases
from openai import OpenAI

class OpenAIParser():


    def __init__(self, openai_api, model_name = "gpt-5-nano", temperature = 0.1):
        self.api_key = openai_api
        self.model_name = model_name
        self.temperature = temperature

        self.instruction = release_notes_parser_instructions

        self.client = OpenAI(
            api_key=self.api_key,
        )

        # Properties
        self._name, self._version = "Gemini", "N/A"
        self._description = "Gemini Parser."


    def call_parser(self, content):

        response = self.client.responses.parse(
            model=self.model_name,
            instructions=self.instruction,
            input=content,
            text_format=Releases,
        )

        return response


    def parse(self, content):
        raw_response = self.call_parser(content)

        return raw_response.output_parsed

