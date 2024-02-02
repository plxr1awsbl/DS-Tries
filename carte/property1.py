import os
import requests


class Property():
    
    property_id : str
    title       : str
    bedrooms    : int
    images      : list
    _price      : int
    district    : str
    region      : str
    url         : str
    
    def __init__(self, jsn: dict) -> None:
        self.property_id = jsn['id']
        self.title       = jsn['title'].replace('/', '.')
        self.bedrooms    = jsn['bedrooms']
        self.district    = jsn['district']
        self.price       = jsn['price']
        self.url         = jsn['url']
        self.region      = jsn['region']
        
        img  = list(jsn['image'])
        imgs = list(jsn['images'])
        img.extend(imgs)
        self.images = img
        
    @property
    def price(self):
        return self._price if self._price > 0 else "по запросу"
    
    @price.setter
    def price(self, val: str):
        try:
            val = int(val)
            self._price = val
        except ValueError:
            self._price = 0
    
    def __str__(self) -> str:
        text = "{title}\n\nCпален {bedrooms}\nРайон {district}\nРегион {region}\nЦена {price}\n\n{url}".format(
            title=    self.title,
            price=    self.price,
            district= self.district,
            url=      self.url,
            region=   self.region,
            bedrooms= self.bedrooms
        )
        
        return text
    
    def to_file(self, path: str):
        with open(path, 'w+') as f:
            f.write(str(self))

    
    def to_pack(self, path: str):
        n_path  = path + self.title
        os.mkdir(n_path)
        
        f_path  = n_path + '/{title}.txt'.format(title=self.title)
        self.to_file(f_path)
        
        ph_path = n_path + '/photos'
        os.mkdir(ph_path)