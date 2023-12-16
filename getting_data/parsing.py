import requests
import re

from bs4 import BeautifulSoup
from typing import Dict, Set


# Finds mentions of keyword in text html p tags 
def paragraph_mentions(text: str, keyword: str) -> bool:
    soup = BeautifulSoup(text, "html5lib")
    paragraphs = [p.get_text for p in soup['p']]
    
    return any(keyword.lower() in paragraph.lower() for paragraph in paragraphs)

regex = r"^https?://.*\.house\.gov/?$" # Regular expression for representatives' links

url  = "https://www.house.gov/representatives"
text = requests.get(url).text
soup = BeautifulSoup(text, "html5lib")

all_urls = [a['href'] for a in soup('a') if a.has_attr('href')]

good_urls = [url for url in all_urls if re.match(regex, url)]
good_urls = list(set(good_urls)) # We use set to throw out duplicated links

press_releases: Dict[str, Set[str]] = {}

for house_url in good_urls:
    html = requests.get(house_url).text
    soup = BeautifulSoup(text, "html5lib")
    
    pr_links = {a['href'] for a in soup('a') if 'press release' in a.text.lower()}
    # print(f"{house_url}: {pr_links}")
    press_releases[house_url] = pr_links

for house_url, pr_links in press_releases.items():
    for pr_link in pr_links:
        url = f"{house_url}/{pr_link}"
        text = requests.get(url).text
        if paragraph_mentions(text, 'data'):
            print(f"{house_url}")
            break