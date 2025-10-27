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
    source_url: Optional[str] | None = Field(
        None, 
        description="The official URL pointing to the release notes or repository for this SDK version.")

class Releases(BaseModel):
    releases: List[Release] = Field(..., description="Release List")

class SDKReleaseNotesScraperResult(BaseModel):
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

# For Metadata Extractor:

class ExampleApp(BaseModel):
    name: Optional[str] = Field(None, description="Name of the mobile app using this SDK.")
    developer: Optional[str] = Field(None, description="Developer of the mobile app using this SDK.")
    url: Optional[str] = Field(None, description="Links to the reference of the mobile app.")

class MetadataSchema(BaseModel):
    purpose: Optional[str] = Field(
        None,
        description="A concise explanation of what the SDK is used for."
    )
    developer: Optional[str] = Field(
        None,
        description="The company or organization that developed the SDK."
    )
    initial_release_date: Optional[str] = Field(
        None,
        description="The initial release date of the SDK in YYYY-MM-DD format."
    )
    key_features: Optional[List[str]] = Field(
        default_factory=list,
        description="A short list of key features or capabilities of the SDK."
    )
    license_type: Optional[str] = Field(
        None,
        description="The type of license (open source, proprietary, freemium, or other)."
    )
    documentation_url: Optional[str] = Field(
        None,
        description="Link to the official documentation of the SDK."
    )
    platforms: Optional[List[str]] = Field(
        default_factory=list,
        description="Supported platforms (iOS, Android, cross-platform, etc.)."
    )
    example_apps: Optional[List[ExampleApp]] = Field(
        default_factory=list,
        description="Example mobile apps that use this SDK."
    )
    source_urls: Optional[List[str]] = Field(
        default_factory=list,
        description="List of authoritative source URLs used for extracting the information."
    )

class SDKMetadataScraperResult(BaseModel):
    """

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
    metadata: MetadataSchema = Field(
        ...,
        description="The time invariant metadata of the SDK."
    )

# Final Schema for one SDK:

class SDK(BaseModel):
    """

    """
    index: int = Field(),
    sdk_name: str = Field(),
    platform: List[str] = Field(),
    android_id_from_ios_perspective: str = Field(),
    ios_id: str = Field(),
    android_id: str = Field(),
    ios_id_from_android_perspective: str = Field(),
    company: str = Field(),
    android_totins: str = Field(),
    ios_totins: str = Field(),
    totins: str = Field(),
    function: str = Field(),
    platforms: str = Field(),
    url: str = Field(),

    metadata: SDKMetadataScraperResult = Field(
        ...,
        description="The time invariant metadata of the SDK of a specific scraper."
    )
    repository_url: List[str] = Field(
        ...,
        description="Link to the official repository URL of the SDK (if available)."
    )
    release_notes_url: List[str] = Field(
        ...,
        description="Link to the official release notes webpage URL found in the SDK documentation (if available)."
    )
    all_release_notes: List[SDKReleaseNotesScraperResult] = Field(
        ...,
        description="All the release notes of the SDK of several scrapers."
    )


# For Linkup

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