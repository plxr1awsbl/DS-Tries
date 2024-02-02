import requests

from myparser import ParserCarte
from property1 import Property



PATH = "/Users/bogdankoinov/Desktop/Работа/Недвижка/"


p = ParserCarte(PATH)



for i in range(30):
    Property(p.json_list[i]).to_pack(PATH+'carte/')
