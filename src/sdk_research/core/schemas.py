from pydantic import BaseModel, Field
from typing import List, Optional


# ----- Release Notes Models ----- #

class Release(BaseModel):
    version: str = Field(
        ..., 
        description="The semantic version number of the SDK release (e.g., 'v2.12.0')."
    )
    release_date: str = Field(
        ..., 
        description="The official release date of this version in YYYY-MM-DD format."
    )
    notes: str = Field(
        ..., 
        description="A concise summary of the changes, improvements, or fixes in this release."
    )
    source_url: str | None = Field(
        None, 
        description="The official URL pointing to the release notes or repository for this SDK version.")
    
# class SDKReleases(BaseModel):
#     content: List[Release] = Field(
#         ..., 
#         description="A list of SDK release entries, each containing version, release_date, notes, and optional source_url."
#     )

class SDKScraperResult(BaseModel):
    """
    Result from a specific SDK scraper engine.
    """
    extractor_name: str = Field(
        ..., 
        description="The name of the scraper engine that produced this result."
    )
    extractor_version: str = Field(
        ..., 
        description="The version of the scraper engine (e.g., '1.0.0')."
    )
    sdk_name: str = Field(
        ...,
        description="The name of the SDK."
    )
    platform: str = Field(
        ...,
        description="The platform of the SDK (eg. Android, iOS), if applicable."
    )
    truncated: str = Field(
        ...,
        description="Whether if the release notes are truncated or not."
    )
    releases: List[Release] = Field(
        ..., 
        description="A list of SDK release entries, each containing version, release_date, notes, and optional source_url."
    )

class AllScrapperResults(BaseModel):
    """
    A collection of results from multiple scraper engines.
    """
    results: List[SDKScraperResult] = Field(
        ..., 
        description="A list of scraper results, each containing metadata about the scraper and the SDK releases it found."
    )


# For Structured Output (if needed)

from typing import List, Optional
from pydantic import BaseModel, Field

class ExampleApp(BaseModel):
    name: str = Field(..., description="Name of the mobile app using this SDK.")
    developer: Optional[str] = Field(..., description="Developer of the mobile app using this SDK.")
    url: Optional[str] = Field(..., description="Links to the reference of the mobile app.")

class MetadataStructuredOutput(BaseModel):
    purpose: str = Field(
        ...,
        description="A concise explanation of what the SDK is used for."
    )
    developer: str = Field(
        ...,
        description="The company or organization that developed the SDK."
    )
    initial_release_date: Optional[str] = Field(
        ...,
        description="The initial release date of the SDK in YYYY-MM-DD format, or null if unknown."
    )
    key_features: List[str] = Field(
        ...,
        description="A short list of key features or capabilities of the SDK."
    )
    license_type: Optional[str] = Field(
        None,
        description="The type of license (open source, proprietary, freemium, or other)."
    )
    platforms: List[str] = Field(
        default_factory=list,
        description="Supported platforms (iOS, Android, cross-platform, etc.)."
    )
    example_apps: List[ExampleApp] = Field(
        default_factory=list,
        description="Example mobile apps that use this SDK."
    )
    source_urls: List[str] = Field(
        default_factory=list,
        description="List of authoritative source URLs used for extracting the information."
    )

# Linkup

linkup_schema = """{
  "type": "object",
  "properties": {
    "versions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "version": { "type": "string" },
          "release_date": { "type": "string" },
          "notes": { "type": "string" }
        }
      }
    }
  }
}"""


# class MetadataStructuredOutput(BaseModel):
#     purpose: str = Field(
#         ...,
#         description="A concise explanation of what the SDK is used for."
#     )
#     developer: str = Field(
#         ...,
#         description="The company or organization that developed the SDK."
#     )
#     initial_release_date: str = Field(
#         ...,
#         description="The initial release date of the SDK in YYYY-MM-DD format, or null if unknown."
#     )
#     key_features: str = Field(
#         ...,
#         description="A short list of key features or capabilities of the SDK."
#     )
#     license_type: str = Field(
#         ...,
#         description="The type of license (open source, proprietary, freemium, or other)."
#     )
#     platforms: str = Field(
#         ...,
#         description="Supported platforms (iOS, Android, cross-platform, etc.)."
#     )
#     example_apps: str = Field(
#         ...,
#         description="Example mobile apps that use this SDK."
#     )
#     source_urls: str = Field(
#         ...,
#         description="List of authoritative source URLs used for extracting the information."
#     )