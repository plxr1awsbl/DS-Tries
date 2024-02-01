import requests
import os
import urllib

from bs4 import BeautifulSoup
from dataclasses import dataclass


class Property():
    
    info: dict 

    def __init__(self, url: str, path: str) -> None:
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'html5lib')
        
        try:
            title    = soup.find('h1', 'object-page__title').find('strong').text
        except AttributeError:
            title    = None
        try:
            spans    = soup.find('div', 'object-page__icon-block').text.split('\n')
            type_    = spans[1].split()[0]
            try:
                bedrooms = int(spans[2].split()[0])
            except ValueError:
                bedrooms = spans[2].split()[0]
            location = spans[3].split()[0]
            to_beach = spans[4] 
        except AttributeError:
            location = None
            bedrooms = None
            type_    = None
            to_beach = None
        try:
            wys_text = soup.find('div', 'wys_text').text
        except AttributeError:
            wys_text = None
        
        self.info = {
            'title'    : title if title else "None",
            'type'     : type_ if type_ else "None",
            'bedrooms' : bedrooms if bedrooms else "None",
            'location' : location if location else "None",
            'to_beach' : to_beach if to_beach else "None",
            'wys'      : wys_text if wys_text else "None",
            'url'      : url
        }
        
        self._make_path(path=path)
        
    def _make_path(self, path):
        
        folder_path = "{path}/{title}"
        file_path   = "{path}/{title}/{title}.txt"
        photo_path  = "{path}/{title}/photos"
        
        self.path = {
            "path" : path,
            "folder" : folder_path.format(path=path, title=self.info['title']),
            "file"   : file_path.format(path=path, title=self.info['title']),
            "photos"  : photo_path.format(path=path, title=self.info['title'])}
    
    
    def _to_file(self):
        text = "{title}\n\n{type}\n{location}\n{bedrooms} спален\n{to_beach}\n\n{url}\n\n{wys}"
        
        with open(self.path['file'], 'w') as f:
            f.write(text.format(
                title   =self.info['title'],
                location=self.info['location'],
                type    =self.info['type'],
                bedrooms=self.info['bedrooms'],
                to_beach=self.info['to_beach'],
                url     = self.info['url'],
                wys     =self.info['wys']
                ))
    
    def _error_file(self):
        text = "Ошибочный файл был создан из-за повтора\n\n\n{title}\n\n{type}\n{location}\n{bedrooms} спален\n{to_beach}\n\n{url}\n\n{wys}"
        
        path = self.path['path'] + '/errorfile.txt'
        
        with open(path, 'w+') as f:
            f.write(text.format(
                title   =self.info['title'],
                location=self.info['location'],
                type    =self.info['type'],
                bedrooms=self.info['bedrooms'],
                to_beach=self.info['to_beach'],
                url     = self.info['url'],
                wys     =self.info['wys']
                ))
    
    def to_pack(self):
        try:
            os.mkdir(self.path['folder'])
            os.mkdir(self.path['photos'])
            self._to_file()
        except FileExistsError:
            self._error_file()

