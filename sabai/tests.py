from property_model import Property
from utils import get_object_urls
from bs4 import BeautifulSoup
import requests


urls = get_object_urls()

for url in urls:
    p = Property(url, path='/Users/bogdankoinov/Desktop/Работа/Недвижка/text')
    p.to_pack()