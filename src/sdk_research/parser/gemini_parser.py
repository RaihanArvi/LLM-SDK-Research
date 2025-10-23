from src.sdk_research.core.prompts import release_notes_parser_instructions
from src.sdk_research.core.schemas import Release
from google import genai
from google.genai import types
import json

class GeminiParser():

    def __init__(self, gemini_api, model_name = "gemini-flash-lite-latest", temperature = 0.1):
        self.api_key = gemini_api
        self.model_name = model_name
        self.temperature = temperature

        self.instruction = release_notes_parser_instructions

        self.client = genai.Client(
            api_key=self.api_key,
        )

        # Properties
        self._name, self._version = "Gemini", "N/A"
        self._description = "Gemini Parser."


    def call_parser(self, content):

        model = self.model_name
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=content),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=self.temperature,
            thinking_config = types.ThinkingConfig(
                thinking_budget=0,
            ),
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type = genai.types.Type.OBJECT,
                required = ["Releases"],
                properties = {
                    "Releases": genai.types.Schema(
                        type = genai.types.Type.ARRAY,
                        items = genai.types.Schema(
                            type = genai.types.Type.OBJECT,
                            required = ["version", "release_date", "notes"],
                            properties = {
                                "version": genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                                "release_date": genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                                "notes": genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            },
                        ),
                    ),
                },
            ),

            system_instruction=[
                types.Part.from_text(text=self.instruction),
            ],
        )

        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )

        return response


    def validate_model(self, response):
        releases_dict = json.loads(response.text)

        try:
            list_release = [Release.model_validate(release) for release in releases_dict['Releases']]
            return list_release
        except Exception as e:
            r = Release(
                version = "PARSING ERROR.",
                release_date= "PARSING ERROR.",
                notes = "PARSING ERROR.",
            )
            return r


    def parse(self, content):
        raw_response = self.call_parser(content)
        list_release = self.validate_model(raw_response)

        return list_release

