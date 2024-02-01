import requests
import os
import urllib

from bs4 import BeautifulSoup
from dataclasses import dataclass


url = "https://villacarte.com/en/rent?limit=24&location=phuket&type=villa"
    #   "https://villacarte.com/en/rent?limit=24&location=phuket&page=2&type=villa"
text = requests.get(url).text
soup = BeautifulSoup(text, "html5lib")

