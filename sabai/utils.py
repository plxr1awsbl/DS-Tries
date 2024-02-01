import requests
from bs4 import BeautifulSoup


def get_object_urls():
    url = "https://www.sabai-house.com/catalog/nedvizhimost/?for_sale=0"
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html5lib")

    # object_links = soup('a', 'object-item__img-block')
    object_links = ['https://www.sabai-house.com' + a.get('href') for a in soup('a') if 'object-item__img-block' in a.get('class', [])]
    
    return set(object_links)

