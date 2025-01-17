from fastapi import FastAPI, Query
from typing import List, Optional
import requests as rq
import pandas as pd
import json

app = FastAPI()

@app.get("/")
def status():
    return {'Status':'Working'}


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

        city = data[0]['name']
        region = data[0]['address']['state']
        province = data[0]['address']['ISO3166-2-lvl6'][-2:]

        full = {'citta':city,
                'regione':region,
                'provincia':province}
        
        return full
    
    full_city = enrich_city(citta)

    res = rq.get(
        f'https://www.immobiliare.it/api-next/search-list/real-estates/?fkRegione={full_city['regione']}&idProvincia={full_city['provincia']}&idNazione=IT&__lang=it&idContratto=1&idCategoria=1&pag={page}&path=%2Fvendita-case%2F{full_city['citta']}%2F'
    )
    data = res.json().get('results', [])
    collection = []

    for item in data:
        immobiliare = { 'title':str,
                        'price':int,
                        'surface':int,
                        'floor':int,
                        'rooms':int,
                        'condition':str,
                        'bathrooms':str,
                        'type':str,
                        'elevator':str,
                        'garage':str,
                        'address':str,
                        'img':str,
                        'id':int,
                        'source':'immobiliare.it'
                        }
                        
        try:
            immobiliare['price'] = item['realEstate']['price']['value']
            immobiliare['title'] = item['realEstate']['title']
            immobiliare['surface'] = item['realEstate']['properties'][0]['surface'].strip(' m²')
            immobiliare['condition'] = item['realEstate']['properties'][0]['ga4Condition']
            immobiliare['bathrooms'] = item['realEstate']['properties'][0]['bathrooms']
            immobiliare['type'] = item['realEstate']['properties'][0]['typology']['name']
            immobiliare['elevator'] = item['realEstate']['properties'][0]['elevator']
            immobiliare['garage'] = item['realEstate']['properties'][0]['ga4Garage']
            immobiliare['floor'] = item['realEstate']['properties'][0]['floor']['abbreviation']
            immobiliare['rooms'] = item['realEstate']['properties'][0]['rooms']
            immobiliare['address'] = str(item['realEstate']['properties'][0]['location']['address']+', '+item['realEstate']['properties'][0]['location']['city'])
            immobiliare['img'] = item['realEstate']['properties'][0]['multimedia']['photos'][0]['urls']['small']
            immobiliare['id'] = item['realEstate']['id']
            immobiliare['link'] = 'https://www.immobiliare.it/annunci/' + str(immobiliare['id'])
            collection.append(immobiliare)
        except:
            pass

    return collection


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


@app.get("/listings/")
def listings(citta:str,page:int=1):
    immobiliare = get_immobiliare(citta,page=page)
    casa = casait(citta,page=page)
    tot = immobiliare+casa
    data = sorted(tot, key=lambda x: x["price"],reverse=True)
    return data


@app.get("/listing_url/")
def listing_id(url:str):
    import requests as rq
    from bs4 import BeautifulSoup as bs
    import json

    res = rq.get(url)
    soup = bs(res.content,'html5lib')

    if 'immobiliare' in url:

        listing = {
            'title':str,
            'price':int,
            'img':str,
            'address':str,
            'coords':[]
        }

        data = json.loads(soup.find('script',{'type':'application/json'}).string)

        listing['title'] = data['props']['pageProps']['detailData']['realEstate']['title']
        listing['price'] = data['props']['pageProps']['detailData']['realEstate']['price']['value']
        listing['img'] = data['props']['pageProps']['detailData']['realEstate']['properties'][0]['multimedia']['photos'][0]['urls']['large']
        location_data = data['props']['pageProps']['detailData']['realEstate']['properties'][0]['location']

        listing['address'] = location_data['address'] + ' ' + location_data['streetNumber'] + ', ' + location_data['city']
        listing['coords'] = location_data['latitude'], location_data['longitude']
                

        return listing

    elif 'casa.it' in url:
        pass