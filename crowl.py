import openpyxl
from bs4 import BeautifulSoup
import time
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font, Alignment
from selenium import webdriver
import Addon
cur_index = 2
cnt = 0

class ListShopMall:
    def __init__(self):
        self.col_dic = {}
        self.book = openpyxl.Workbook()
        self.sheet = self.book.active

        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get("https://search.shopping.naver.com/mall/mall.nhn")
        self.driver.implicitly_wait(3)

    def setColumn(self, col_dic, col_width):
        i = 0
        self.sheet.row_dimensions[1].height = 30
        self.col_dic = col_dic
        for key,value in col_dic.items():
            self.sheet[key+'1'].value = value
            # self.sheet[key + '1'].border = 1
            self.sheet[key + '1'].font = Font(size=13, bold=True)
            self.sheet.column_dimensions[key].width = col_width[i]
            self.sheet.alignment = Alignment(horizontal='center', vertical='center')
            i += 1

    def scrapOnePage(self, page):
        global cur_index, cnt

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('tr')

        for card in cards:
            try:
                mall_name = card.find('img').attrs['alt']
                rank = card.find('span', class_="grade").text
                link = card.find('td', class_='url').find('p').find('a').text
                count = card.find('td', class_='item').find('strong').find('a').text

                if (rank == '빅파워' or rank == '프리미엄' or rank == '플레티넘') and (int(count) <= 30):
                    total, today = Addon.Visitor.getVisitors(link)
                    item_name, price, review_cnt, buy_cnt = Addon.Item.bestItem(mall_name)
                    self.sheet['A' + str(cur_index)] = rank
                    self.sheet['B' + str(cur_index)] = today
                    self.sheet['C' + str(cur_index)] = count
                    self.sheet['D' + str(cur_index)] = mall_name
                    self.sheet['E' + str(cur_index)] = 0
                    self.sheet['F' + str(cur_index)] = item_name
                    self.sheet['G' + str(cur_index)] = price
                    self.sheet['H' + str(cur_index)] = review_cnt
                    self.sheet['I' + str(cur_index)] = buy_cnt
                    self.sheet['J' + str(cur_index)] = price * buy_cnt
                    self.sheet['K' + str(cur_index)] = (price * buy_cnt)

                    print(mall_name, rank, link, count, total, today, item_name, price, review_cnt, buy_cnt, price*buy_cnt)
                    # print(mall_name, " -> ", rank, count, total, today, item_name, price, review_cnt, buy_cnt, price * buy_cnt, (price * buy_cnt))
                    cur_index += 1

            except Exception as e:
                # print(e)
                pass

    def nextPage(self, dest):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        cmd = "mall.changePage(%d, 'listPaging');" % dest
        print("========================== %d ==========================" % dest)
        self.driver.execute_script(cmd)
        # time.sleep(1)
        cur_page = soup.find_all('div',{'id':'listPaging'})[0].find('strong').text

    def MakeList(self, page=1000):
        for i in range(1,page):
            self.scrapOnePage(1)
            self.nextPage(i + 1)

    def Save(self, xlsx_loc):

        self.book.save(xlsx_loc)
        self.book.close()

if __name__ == "__main__":
    Addon.driverRe()
    list = ListShopMall()
    list.setColumn({"A": "몰등급", "B": "일평균 방문자수", "C": "상품개수","D": "스토어명", "E": "카테고리", "F": "베스트 상품",
                           "G": "가격",  "H": "리뷰수", "I": "일 평균 추정 주문량", "J":" 단일 상품 추정 매출", "K": "순이익 (30% 마진)",
                           "L": "남자", "M": "여자", "N": "1위"}, [10, 15, 10, 25, 10, 13, 10, 10, 20, 20, 20, 10, 10, 10])

    list.MakeList(page=10)
    list.Save("./result.xlsx")
