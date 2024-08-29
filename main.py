from bs4 import BeautifulSoup
import re
import requests
import json
import xml.etree.ElementTree as ET

# Returned 400 or 500, check later
bad_links = ['/stig/mobile_device_management_mdm_server_security_requirements_guide/',
             '/stig/operating_system_policy_security_requirements_guide_unix_version/',
             '/stig/operating_system_security_requirements_guide_unix_version/',
             '/stig/symantec_antivirus_locally_configured_client/',
             '/stig/symantec_antivirus_managed_client/',
             '/stig/web_server_security_requirements_guide/']

def find_stig_links(url):
  try:
      # Send a GET request to the URL
      response = requests.get(url)
      response.raise_for_status()  # Check for HTTP errors

      # Parse the HTML content using BeautifulSoup
      soup = BeautifulSoup(response.text, 'html.parser')

      # Find all <a> tags with href attribute matching the pattern
      stig_links = []
      for a_tag in soup.find_all('a', href=True):
          href = a_tag['href']
          if href in bad_links:
              continue
          if re.match(r'^/stig/.*$', href) and href not in bad_links:
            try:
              # Send a GET request to the URL
              response = requests.get('https://www.stigviewer.com' + href)
              response.raise_for_status()  # Check for HTTP errors

              # Parse the HTML content using BeautifulSoup
              soup = BeautifulSoup(response.text, 'html.parser')

              # Find all <a> tags with href attribute ending with /xml
              for a_tag in soup.find_all('a', href=True):
                  href = a_tag['href']
                  # Check if href ends with /xml
                  if href.endswith('/xml'):
                      stig_links.append(href)
                      #print(href)
            except requests.RequestException as e:
              print(f"An error occurred: {e}")
              return []

      return stig_links

  except requests.RequestException as e:
      print(f"An error occurred: {e}")
      return []

def get_stig_name(stig_link):
  
  # Remove "/stig/" from the start
  if stig_link.startswith("/stig/"):
    stig_link= stig_link[len("/stig/"):]

  # Remove "/" from the end if it exists
  if stig_link.endswith("/"):
    stig_link = stig_link[:-1]
  
  stig_name = stig_link
 
  return stig_name
  
def get_stig_versions(links):
    
  versions = {}
  ns = {'ns': 'http://checklists.nist.gov/xccdf/1.1'}
    
  for link in links:
    xml_content = requests.get('https://www.stigviewer.com' + link).text
    try:
          # Parse the XML content
        root = ET.fromstring(xml_content)

          # Extract ID from the Benchmark element
        benchmark_id = root.get('id', None)

          # Extract version number
        version_element = root.find('ns:version', namespaces=ns)
        version = version_element.text if version_element is not None else 'Not found'
          #version = root.find('version', None).text.strip()
        plain_text_element = root.find('ns:plain-text', namespaces=ns)
        if plain_text_element is not None:
            release_info = plain_text_element.text
        if release_info:
              # Extract release from the release_info text
            try:
              release = release_info.split('Release:')[1].split()[0]
            except IndexError:
              release = 'Release info format error'

          # Parse release info to get release number and date
        if release_info:
            parts = release_info.split(' ')
            try:
                release_number = parts[1]
                date = ' '.join(parts[4:])
            except IndexError:
                raise ValueError("Release info format is unexpected.")

        versions[benchmark_id] = f"V{version}R{release_number}"

    except ET.ParseError as e:
        print(f"XML parsing error: {e}")
    except AttributeError as e:
        print(f"Error finding XML elements: {e}")
          
  return versions
    
# Base URL, don't change unless site changes
url = 'https://www.stigviewer.com/stigs'

# Get all links from the base URL
links = find_stig_links(url)

# Get the stig version and release
stig_versions = get_stig_versions(links)

#print for now, write to file/store as dict when second part is ready
print(json.dumps(stig_versions,indent=3))
