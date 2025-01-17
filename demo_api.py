from fastapi import FastAPI, Query
from typing import List, Optional
import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs

app = FastAPI()

@app.get("/")
def status():
    return {'Status':'Working'}

@app.get('/immobiliare/')
def get_immobiliare(
    citta: str,
    page: int = 1):
    
    def enrich_city(city:str):
        import requests
        headers = {
            'accept': '*/*',
            'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'dnt': '1',
            'priority': 'u=1, i',
            'referer': 'https://nominatim.openstreetmap.org/ui/search.html?q=Napoli&format=json&addressdetails=1&limit=1',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        params = {
            'q': city,
            'limit': '1',
            'format': 'jsonv2',
            'addressdetails':'1'
        }

        response = requests.get('https://nominatim.openstreetmap.org/search', params=params, headers=headers)

        data = response.json()

        citta = data[0]['name']
        region = data[0]['address']['state']
        province = data[0]['address']['ISO3166-2-lvl6'][-2:]

        full = {'citta':citta,
                'regione':region,
                'provincia':province}
        
        return full
    
    return enrich_city(citta)
    

@app.get('/casa/')
def casait(citta:str,page:int=1):
    cookies = {
        'didomi_token': 'eyJ1c2VyX2lkIjoiMTk0MTQ3ZmYtZmNhYy02ZGNkLWI5ZmYtMTk1N2QzYTJjYzZjIiwiY3JlYXRlZCI6IjIwMjQtMTItMjlUMjI6MTg6NDAuNDU4WiIsInVwZGF0ZWQiOiIyMDI0LTEyLTI5VDIyOjE4OjQyLjQ4M1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOm1pY3Jvc29mdCJdfSwicHVycG9zZXMiOnsiZW5hYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZXJzaW9uIjoyLCJhYyI6IkFGbUFDQUZrLkFBQUEifQ==',
        'euconsent-v2': 'CQKZaoAQKZaoAAHABBENBSFoAP_AAAAAABCYGMwCQAIAAgABaADIAGgARAAtgLzAYyAAAAYdABgACCqhaADAAEFVCUAGAAIKqFIAMAAQVUIQAYAAgqoEgAwABBVQ.f_gAAAAAAAAA',
        '_gcl_au': '1.1.1185159061.1735510723',
        'g_state': '{"i_p":1735936797624,"i_l":2}',
        'datadome': 'JVL0ssjTBheLiICWKtGn60lC_HyKuokkuysRrFKnQGYWVdEUDXAcbZ3fEG5JYQwCRgOlA~4rDfdXAk1zHPBTqY8koCQ_u2y5LzD2fFECgXx~jlWEmjHb9lM~mppd~rH4',
        'utag_main__sn': '4',
        'utag_main_ses_id': '1735913458165%3Bexp-session',
        'utag_main__prevVtUrl': 'https%3A%2F%2Fwww.casa.it%2F%3Bexp-1735917058239',
        'utag_main__prevVtUrlReferrer': '%3Bexp-1735917058239',
        'utag_main__prevVtSource': 'Direct traffic%3Bexp-1735917058239',
        'utag_main__prevVtCampaignName': 'organicWeb%3Bexp-1735917058239',
        'utag_main__ss': '0%3Bexp-session',
        'utag_main__se': '16%3Bexp-session',
        'utag_main__st': '1735915401769%3Bexp-session',
        'utag_main__pn': '16%3Bexp-session',
        'utag_main__prevTrackView': 'viewResults > portal > listing > resultList%3Bexp-1735917202094',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'cookie': 'didomi_token=eyJ1c2VyX2lkIjoiMTk0MTQ3ZmYtZmNhYy02ZGNkLWI5ZmYtMTk1N2QzYTJjYzZjIiwiY3JlYXRlZCI6IjIwMjQtMTItMjlUMjI6MTg6NDAuNDU4WiIsInVwZGF0ZWQiOiIyMDI0LTEyLTI5VDIyOjE4OjQyLjQ4M1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOm1pY3Jvc29mdCJdfSwicHVycG9zZXMiOnsiZW5hYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZXJzaW9uIjoyLCJhYyI6IkFGbUFDQUZrLkFBQUEifQ==; euconsent-v2=CQKZaoAQKZaoAAHABBENBSFoAP_AAAAAABCYGMwCQAIAAgABaADIAGgARAAtgLzAYyAAAAYdABgACCqhaADAAEFVCUAGAAIKqFIAMAAQVUIQAYAAgqoEgAwABBVQ.f_gAAAAAAAAA; _gcl_au=1.1.1185159061.1735510723; g_state={"i_p":1735936797624,"i_l":2}; datadome=JVL0ssjTBheLiICWKtGn60lC_HyKuokkuysRrFKnQGYWVdEUDXAcbZ3fEG5JYQwCRgOlA~4rDfdXAk1zHPBTqY8koCQ_u2y5LzD2fFECgXx~jlWEmjHb9lM~mppd~rH4; utag_main__sn=4; utag_main_ses_id=1735913458165%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.casa.it%2F%3Bexp-1735917058239; utag_main__prevVtUrlReferrer=%3Bexp-1735917058239; utag_main__prevVtSource=Direct traffic%3Bexp-1735917058239; utag_main__prevVtCampaignName=organicWeb%3Bexp-1735917058239; utag_main__ss=0%3Bexp-session; utag_main__se=16%3Bexp-session; utag_main__st=1735915401769%3Bexp-session; utag_main__pn=16%3Bexp-session; utag_main__prevTrackView=viewResults > portal > listing > resultList%3Bexp-1735917202094',
        'dnt': '1',
        'origin': 'https://www.casa.it',
        'priority': 'u=1, i',
        'referer': 'https://www.casa.it/vendita/residenziale/roma?page=2&sortType=price_desc',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    res = rq.get(f'https://www.casa.it/vendita/residenziale/{citta}?sortType=price_desc&page={page}',cookies=cookies,headers=headers)

    from bs4 import BeautifulSoup as bs

    soup = bs(res.content,'html5lib')

    cards = soup.find_all('div',class_='grid csaSrpcard__inner grid')

    data = []

    for card in cards:

        listing = {
                'title':str,
                'price':int,
                'surface':int,
                'img':str,
                'link':str,
                'source':'casa.it'
            }

        listing['title'] = (card.find('a',class_='csaSrpcard__det__title--a c-txt--f0').text)
        listing['price'] = int(card.find('span',class_='csaSrpcard__det__feats--price tp-w--l').text.replace('.',''))
        listing['surface'] =  (card.find_all('span',class_='csaSrpcard__det__feats__item')[0].text.replace(' mq',''))
        listing['link'] = ('https://www.casa.it' + card.find('a',class_='csaSrpcard__det__title--a c-txt--f0')['href'])
        try:
            listing['img'] = bs(rq.get(listing['link'],headers=headers,cookies=cookies).content,'html5lib').find('picture',class_='pdp-newgal__pic is-rel is-clickable').find('img')['src']
        except:
            listing['img'] = None
        data.append(listing)
    
    return data