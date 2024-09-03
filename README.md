# stigScrape

## Description
This Python script is designed to scrape and process the latests versions of Security Technical Implementation Guides (STIGs) from the website "stigviewer.com". 
Here's a summary of what it does:
1.	Fetch Webpage: Downloads the main STIG page and extracts links to individual STIG documents.
2.	Filter Links: Excludes known bad links and identifies links to XML files.
3.	Extract STIG Information: For each XML file, retrieves and parses data to extract STIG version and release details.
4.	Output Results: Formats and prints the extracted STIG information as a JSON object.

## Intended Workflow:
1. The script runs and collects the latest versions
2. Versions from STIG Manager are collected
3. The current versions are compared against the used versions
4. Differences in versions are reported, identifying out of date STIG usage 
