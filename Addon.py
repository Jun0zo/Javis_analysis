import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup


false = 0
true = 1

def driverRe():
    options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
    options.add_argument('headless')  # headless 모드 설정
    options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    # 속도 향상을 위한 옵션 해제
    prefs = {'profile.default_content_setting_values':
                 {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
                    'geolocation': 2, 'notifications': 2,
                    'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                    'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                    'media_stream_camera': 2, 'protocol_handlers': 2,
                    'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                    'push_messaging': 2, 'ssl_cert_decisions': 2,
                    'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                    'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2
                 }
    }

    options.add_experimental_option('prefs', prefs)

def str2int(str_num):
    num = str_num.replace(',','')
    return int(num)

def int2str(num):
    for i, c in enumerate(str(num)[::-1]):
        pass




class Visitor:
    @classmethod
    def getRequestUrl(cls, url):
        r = requests.get(url)
        html = r.text

        try:
            dic_info = re.search('"sellerShopNo":"[0-9]+"', html).group()
            sellerShopperNo = re.search('[0-9]+', dic_info).group()

        except:
            return ''

        return 'https://smartstore.naver.com/main/ajax/status?sellerShopNo=' + str(sellerShopperNo)

    @classmethod
    def getVisitors(cls, link):
        request_url = cls.getRequestUrl('http://' + link)
        if request_url == '':
            return false, false
        r = requests.get(request_url)

        html = r.text
        total_dic = re.search('"total":[0-9]+', html).group()
        total = re.search('[0-9]+', total_dic).group()
        today_dic = re.search('"today":[0-9]+', html).group()
        today = re.search('[0-9]+', today_dic).group()

        return total, today

class Item:
    @classmethod
    def bestItem(cls,target_mall_name):
        url = 'https://search.shopping.naver.com/search/all.nhn?origQuery=바디츄&pagingIndex=1&pagingSize=40&viewType=list&sort=review&frm=NVSHATC&query=' + target_mall_name
        r = requests.get(url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')

        cards = soup.find_all('li', class_='_itemSection')
        for card in cards:
            try:
                item_name = card.find('div', class_='tit').text.strip()
                price = card.find('span', class_='num _price_reload').text.strip()
                mall_name = card.find('p', class_='mall_txt').find('a').text.strip()
                review_cnt = card.find_all('span', class_='etc')[1].find_all('a')[1].find('em').text.strip().replace(' ', '')
                buy_cnt = card.find_all('span', class_='etc')[1].find('a').find('em').text

                #print(item_name, price, review_cnt, buy_cnt)
                if mall_name == target_mall_name:
                    return item_name, str2int(price), review_cnt, str2int(buy_cnt)
            except Exception as e:
                print('Addon.Item  -> ', e)
        return 'NULL', 'NULL'
