# release_notes_pormpt_platform_specific = f"""
# You are an expert research assistant. Your task is to extract and summarize official release notes for the {sdk_name} SDK, specifically for the {platform} version. 

# Goal: Provide a structured summary of all available releases for {sdk_name}.

# Scope: Search only the official GitHub repository for {sdk_name} (preferably using the provided {{repo_url}}; if not provided, identify the most authoritative, non-fork, non-mirror repository). Focus exclusively on the 'Releases' and 'Changelog' sections/pages. Ensure the repository is for the correct {platform} version.

# Criteria/Method: For each release, extract:
# - version (e.g., 'v1.3.0')
# - release_date (ISO 8601 format if available, otherwise null)
# - notes (concise summary of main improvements, fixes, or changes, written in clear, plain language)
# - url (direct link to the GitHub release)

# Instructions:
# - Use only information explicitly present on GitHub; do not infer or invent details.
# - If any field is missing, set it to null.
# - Keep notes short and readable.
# - Ignore forks, mirrors, or unofficial repositories.

# Format: Return a JSON object with this exact structure:
# {
#   "content": [
#     {
#       "version": "...",
#       "release_date": "...",
#       "notes": "...",
#       "url": "..."
#     }
#   ]
# }
# """

# ----- Links Crawler Prompt ----- #

github_link_platform_specific_query = "official github repository link for {sdk_name} sdk {platform} -inurl:fork -inurl:mirror"

github_link_platform_specific_prompt = """
You are an expert research assistant. Your task is to find official GitHub repository link for {sdk_name} SDK, specifically for the {platform} version. 

Goal: Provide an official GitHub repository link for {sdk_name} SDK, specifically for {platform} version.

Scope: Identify the most authoritative and official repository, avoid fork or mirror repository. Focus exclusively on the 'main' section/page. Ensure the repository is for the correct {platform} version.

Instructions:
- Use only information explicitly present on GitHub; do not infer or invent details.
- If any field is missing, set it to null.
- Keep notes short and readable.
- Ignore forks, mirrors, or unofficial repositories.
"""

# General

github_link_general_query = "official github repository link for {sdk_name} sdk -inurl:fork -inurl:mirror"

github_link_general_prompt = """
You are an expert research assistant. Your task is to find official GitHub repository link for {sdk_name} SDK.

Goal: Provide an official GitHub repository link for {sdk_name} SDK.

Scope: Identify the most authoritative and official repository, avoid fork or mirror repository. Focus exclusively on the 'main' section/page.

Instructions:
- Use only information explicitly present on GitHub; do not infer or invent details.
- If any field is missing, set it to null.
- Keep notes short and readable.
- Ignore forks, mirrors, or unofficial repositories.
"""


# Metadata Extractor

metadata_extractor_prompt = """Extract the following fields about {sdk_name} SDK:
- purpose
- developer
- string of initial release date of the SDK (in YYYY-MM-DD format).
- key_features (array of strings)
- documentation URL / official website.
- license_type (one of: "open source", "proprietary", "freemium", or "other")
- platforms (array containing any of: "iOS", "Android", "cross-platform")
- example_apps (2 - 3 example apps using the SDK with name and URL)

Use only authoritative sources (e.g., official documentation, official repository, vendor website, or official package page). For each field, record its URL source in a `source_urls` object that maps field names to URLs (use null if a source isn’t found).

If any value cannot be found, set it to null. Output exactly the JSON structure as specified below.

After forming the JSON output, validate that all required fields and types match the Output Format. If any validation fails, self-correct and re-verify before returning the result.
"""

# metadata_extractor_output_format = """
# ### Output Format
# Return a JSON object with:
# - purpose (string or null)
# - developer (string or null)
# - initial_release_date (string or null)
# - key_features (array of strings or null)
# - license_type ("open source", "proprietary", "freemium", "other", or null)
# - platforms (list of supported platforms, e.g. Android, iOS, cross-platform)
# - example_apps (list of 2-3 objects with fields: app, evidence_url)
# - source_urls (object mapping each field name to a URL or null)
#
# #### Example:
#
# {
#   "purpose": "A cross-platform image processing SDK.",
#   "developer": "Imagix Corp.",
#   "initial_release_date": "2020-08-15",
#   "key_features": ["Fast image filtering", "GPU acceleration"],
#   "license_type": "open source",
#   "platforms": ["iOS", "Android", "cross-platform"],
#   "example_apps": [
#     {
#       "name": "ML Kit sample apps",
#       "url": "https://github.com/googlesamples/mlkit"
#     }
#   ],
#   "source_urls": {
#     "purpose": "https://imagix.dev/docs",
#     "developer": "https://imagix.dev/about",
#     "initial_release_date": "https://github.com/imagix/releases",
#     "key_features": "https://imagix.dev/features",
#     "license_type": "https://github.com/imagix/LICENSE",
#     "platforms": "https://imagix.dev/docs/platforms",
#     "example_apps": null
#   }
# }
#
# Ensure strict adherence to the example structure and field types.
# """

# ----- Release Notes Scraper Website Prompt ----- #

prompt_website_release_notes_platform_specific = """
Retrieve the release notes history for {sdk_name} SDK, specifically for the {platform} version.
Provide a list of 10 versions with emphasis to these criteria:

1. Include the most recent release (latest version).
2. Include all major updates.
3. Include the very first (initial) release.

Parse it into the provided JSON format, with the fields:
"version" : The version number of the release (ex. v1.0.0).
"release_date" : Release date of the corresponding version in YYYY-MM-DD format.
"notes" : A summary of the changes.

Present the versions in descending chronological order (from most recent to oldest).
"""

prompt_website_release_notes_general = """
Retrieve the release notes history for {sdk_name} SDK.
Provide a list of 10 versions with emphasis to these criteria:

1. Include the most recent release (latest version).
2. Include all major updates.
3. Include the very first (initial) release.

Parse it into the provided JSON format, with the fields:
"version" : The version number of the release (ex. v1.0.0).
"release_date" : Release date of the corresponding version in YYYY-MM-DD format.
"notes" : A summary of the changes.

Present the versions in descending chronological order (from most recent to oldest).
"""
