import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup


def bestItem(target_mall_name):
    url = 'https://search.shopping.naver.com/search/all.nhn?origQuery=바디츄&pagingIndex=1&pagingSize=40&viewType=list&sort=review&frm=NVSHATC&query=' + target_mall_name
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    cards = soup.find_all('li', class_='_itemSection')
    for card in cards:
        try:
            print('=====')
            buy_cnt = card.find_all('span', class_='etc')[1].find_all('a')[1].find('em').text.strip().replace(' ', '')

            print(buy_cnt)
        except:
            print('no')
    return 'NULL', 'NULL'

def API2():
    url = "https://openapi.naver.com/v1/datalab/shopping/category/keyword/gender"

    key = "Cxc2yx_hKC1doTw1260A"
    key2 = "gLsl39cmIw"

    payload = '{"' \
                  'startDate": "2017-08-01",' \
                  '"endDate": "2017-09-30",' \
                  '"timeUnit": "month",' \
                  '"category": "50000000",' \
                  '"keyword": "정장",' \
                  '"device": "",' \
                  '"gender": "",' \
                  '"ages": [ ]' \
              '}'

    headers = {
        'X-Naver-Client-Id': key,
        'X-Naver-Client-Secret': key2,
        'Content-Type': 'application/json'
    }


    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

    print(response)

bestItem('오원')