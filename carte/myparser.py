import enum
import requests
import json
import os


class ParserCarte():
    
    class HouseType(enum.Enum):
        villa      = 'villa'
        apartments = 'apartments'
        penthouse  = 'penthouse'
        townhouse  = 'townhouse'

    class Limit(enum.Enum):
        _24 = '24'
        _18 = '18'
        _12 = '12'
    
    class PageOutOfRangeException(Exception):
        
        def __init__(self, value: int) -> None:
            print("Page num cannot be less than 1. Recieved {v}".format(v=value))
    
    BASE_URL = "https://villacarte.com"
    
    cookies = {
    '_ga_HYE0BM44XN'     : 'GS1.1.1706771492.9.1.1706772428.60.0.0',
    'layout'             : 'list',
    'XSRF-TOKEN'         : 'eyJpdiI6IlRQVkgxVGRLZjFnblZBMlhDUHhDWFE9PSIsInZhbHVlIjoib2Y3d2crR2YyV2QrZkh1aHIySkpoYzlWM3ExVk5YXC9zR0MrZFZ3ZkU4cWtGMW9ZaDRHSzRcL09cLzdjTWtnXC9xUFgiLCJtYWMiOiJjM2MwNDY0MWU5NWIzY2FlOGE0OTc4YzY5ZTg1MjZjYTM0OWE0YjU4MmJkYTczNDRkYTZlMTVkYTA3YjRjOGQ3In0%3D',
    'laravel_session'    : 'eyJpdiI6IkRicCtJbnNOVzcxMk5jZElRN0xpbUE9PSIsInZhbHVlIjoiWVwvNVwvZEFzdEx3TEFobXpQS0hiTUFuZTBGdjlUeWRXRWRWejZyU1pRT1ZwNzBCT2twcXRcL3E4bCtcL0Y0b2IxbXMiLCJtYWMiOiI4OGI0MzZkODAzY2MxNDAzNzg5YmRhZGU0YWEwYWEyNWUyYmQwZDBhYTYxOWVjMTVmNmUyOTgyOTg3ZTk1ZWQ4In0%3D',
    '_fbp'               : 'fb.1.1706185461984.855623397',
    '_ga'                : 'GA1.1.483695967.1706185462',
    '_gcl_au'            : '1.1.1780790621.1706185461',
    '_ym_visorc'         : 'w',
    'tmr_lvid'           : 'fc4cadc013b529c154fd34a8781bedaa',
    'tmr_lvidTS'         : '1706185464653',
    'tmr_detect'         : '1%7C1706771493347',
    '_ym_isad'           : '2',
    'dashly_realtime_services_transport': 'wss',
    'dashly_auth_token'  : 'user.1628041581443416532.4563-ab6e9dd352a4d55529a1c7c332f.048bb56436628bcbb769546437ae93b59cb8110bacbb06b1',
    'dashly_device_guid' : '263145d5-ec1d-4153-87c7-5bc485b422bb',
    'dashly_uid'         : '1628041581443416532',
    '_ym_d'              : '1706185472',
    '_ym_uid'            : '1706185472544700667',
    'eloquent_viewable'  : 'eyJpdiI6ImFTTmpBQ0dzbFJjR2pyYUIybXB6WWc9PSIsInZhbHVlIjoiS2R2MW5Jb2k4NUU5cHVYeVl2dHM1OVJrcXYrNTc0cjdaQWVzaXA4R1wvbkJYcE16WXdOMnpOTUNuQTNFT2tFNkxCa1htWHBJQjc2MFlJaDY3d0JnbHppY053bWhMWHFPNmVKcnRsZ1dcLzNMQ0U3WHV1UGZ1SGpvOXRwTjBTU0NYdiIsIm1hYyI6Ijk1M2I3MGYzYmVjNTVmZDYwMDMzNGQyNDMzNDJlYWE0OWI5ZTAwYjgzOWRjMzAyNTY4YTcwYjk0NTU0NDdhNzQifQ%3D%3D',
    'vc_uuid'            : 'ac08812a-270f-4a43-8dd5-a11c42b754d9',
    }

    headers = {
        'Accept'          : '*/*',
        # Requests sorts cookies= alphabetically
        # 'Cookie': '_ga_HYE0BM44XN=GS1.1.1706771492.9.1.1706772428.60.0.0; layout=list; XSRF-TOKEN=eyJpdiI6IlRQVkgxVGRLZjFnblZBMlhDUHhDWFE9PSIsInZhbHVlIjoib2Y3d2crR2YyV2QrZkh1aHIySkpoYzlWM3ExVk5YXC9zR0MrZFZ3ZkU4cWtGMW9ZaDRHSzRcL09cLzdjTWtnXC9xUFgiLCJtYWMiOiJjM2MwNDY0MWU5NWIzY2FlOGE0OTc4YzY5ZTg1MjZjYTM0OWE0YjU4MmJkYTczNDRkYTZlMTVkYTA3YjRjOGQ3In0%3D; laravel_session=eyJpdiI6IkRicCtJbnNOVzcxMk5jZElRN0xpbUE9PSIsInZhbHVlIjoiWVwvNVwvZEFzdEx3TEFobXpQS0hiTUFuZTBGdjlUeWRXRWRWejZyU1pRT1ZwNzBCT2twcXRcL3E4bCtcL0Y0b2IxbXMiLCJtYWMiOiI4OGI0MzZkODAzY2MxNDAzNzg5YmRhZGU0YWEwYWEyNWUyYmQwZDBhYTYxOWVjMTVmNmUyOTgyOTg3ZTk1ZWQ4In0%3D; _fbp=fb.1.1706185461984.855623397; _ga=GA1.1.483695967.1706185462; _gcl_au=1.1.1780790621.1706185461; _ym_visorc=w; tmr_lvid=fc4cadc013b529c154fd34a8781bedaa; tmr_lvidTS=1706185464653; tmr_detect=1%7C1706771493347; _ym_isad=2; dashly_realtime_services_transport=wss; dashly_auth_token=user.1628041581443416532.4563-ab6e9dd352a4d55529a1c7c332f.048bb56436628bcbb769546437ae93b59cb8110bacbb06b1; dashly_device_guid=263145d5-ec1d-4153-87c7-5bc485b422bb; dashly_uid=1628041581443416532; _ym_d=1706185472; _ym_uid=1706185472544700667; eloquent_viewable=eyJpdiI6ImFTTmpBQ0dzbFJjR2pyYUIybXB6WWc9PSIsInZhbHVlIjoiS2R2MW5Jb2k4NUU5cHVYeVl2dHM1OVJrcXYrNTc0cjdaQWVzaXA4R1wvbkJYcE16WXdOMnpOTUNuQTNFT2tFNkxCa1htWHBJQjc2MFlJaDY3d0JnbHppY053bWhMWHFPNmVKcnRsZ1dcLzNMQ0U3WHV1UGZ1SGpvOXRwTjBTU0NYdiIsIm1hYyI6Ijk1M2I3MGYzYmVjNTVmZDYwMDMzNGQyNDMzNDJlYWE0OWI5ZTAwYjgzOWRjMzAyNTY4YTcwYjk0NTU0NDdhNzQifQ%3D%3D; vc_uuid=ac08812a-270f-4a43-8dd5-a11c42b754d9',
        'Accept-Language' : 'en-GB,en;q=0.9',
        'Host'            : 'villacarte.com',
        'User-Agent'      : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
        'Referer'         : 'https://villacarte.com/en/rent?limit=24&location=phuket&page=51&type=villa',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection'      : 'keep-alive',
        'X-CSRF-TOKEN'    : 'byWq4K4SevGfXBGi1AQ2fXhrqFUy7zLFbHpjqgMU',
        'X-Requested-With': 'XMLHttpRequest',
        'X-XSRF-TOKEN'    : 'eyJpdiI6IlRQVkgxVGRLZjFnblZBMlhDUHhDWFE9PSIsInZhbHVlIjoib2Y3d2crR2YyV2QrZkh1aHIySkpoYzlWM3ExVk5YXC9zR0MrZFZ3ZkU4cWtGMW9ZaDRHSzRcL09cLzdjTWtnXC9xUFgiLCJtYWMiOiJjM2MwNDY0MWU5NWIzY2FlOGE0OTc4YzY5ZTg1MjZjYTM0OWE0YjU4MmJkYTczNDRkYTZlMTVkYTA3YjRjOGQ3In0=',
    }

    params: dict = {
        'limit'    : '24',
        'location' : 'phuket',
        'page'     : '1',
        'type'     : 'villa',
    }
    
    JSON_NAME = '_json_list.json'
    
    json_list: list
    
    @property
    def page(self) -> int:
        return int(self.params['page'])
    
    @page.setter
    def page(self, page: int):
        if page >= 1:
            self.params['page'] = str(page)
        else:
            self.params['page'] = '1'

        
    def __init__(self, path: str) -> None:
        self.page = 1
        jsn_p = path + self.JSON_NAME
        
        if not os.path.exists(jsn_p):
            item_list = self._parse_items()
            with open(jsn_p, 'w+') as f:
                json.dump(item_list, f)
        else:
            with open(jsn_p, 'r') as f:
                self.json_list = list(json.load(f))
        
    
    def _parse_page_urls(self) -> list:
        response = requests.get('https://villacarte.com/en/api/rent', params=self.params, cookies=self.cookies, headers=self.headers)
        data = response.json()
        item_list = data.get('collection').get('data')
        url_list = [(self.BASE_URL + dict(item)['url']) for item in item_list]
        
        return url_list
    
    def _parse_urls(self) -> list:
        all_urls = []
        while True:
            page_urls = self._parse_page_urls()
            if page_urls:
                all_urls.extend(page_urls)
                self.page += 1
            else:
                break
        self.page = 1
        
        return all_urls
    
    def _parse_page_items(self) -> list:
        response = requests.get('https://villacarte.com/en/api/rent', params=self.params, cookies=self.cookies, headers=self.headers)
        data = response.json()
        item_list = data.get('collection').get('data')
        item_list = [dict(item) for item in item_list]
        
        return item_list
    
    def _parse_items(self) -> list:
        all_items = []
        while True:
            page_items = self._parse_page_items()
            if page_items != []:
                all_items.extend(page_items)
                self.page += 1
            else:
                break
        
        return all_items