import requests
from bs4 import BeautifulSoup
import csv


def get_data(html, f):
    soup = BeautifulSoup(html, 'html.parser')
    infos = soup.find('ul', {'class': 'resblock-list-wrapper'}).find_all('li')
    for info in infos:
        try:
            name = info.find('div', {'class': 'resblock-name'}).find('a').get_text()				# 楼盘名
            typ = info.find('div', {'class': 'resblock-name'}).find('span').get_text()				# 楼盘类型

			# 楼盘位置
            location = info.find('div', {'class': 'resblock-location'}).find_all('span')
            location2 = info.find('div', {'class': 'resblock-location'}).find('a').get_text()
            if ',' in location2:
                index = location2.index(',')
                location2 = location2[0:index] + ' ' + location2[index + 1:]
                if ',' in location2:
                    index = location2.index(',')
                    location2 = location2[0:index]
            loc_num = len(location)
            loc = ''
            for i in range(0, loc_num):
                loc = loc + location[i].text + ' '
            loc = loc + location2

			# 价格
            price = info.find('div', {'class': 'resblock-price'}).find('div', {'class', 'main-price'}).find_all('span')
            price_num = len(price)
            if price_num == 2:
                pri = int(price[0].text)
                pri_unit = price[1].text[1:]
            else:
                pri = None
                pri_unit = None

            area = info.find('div', {'class': 'resblock-area'}).find('span').get_text()				# 面积

			# 同一价格单位
            if pri_unit is None:
                continue
            elif pri_unit[0] == '万':
                area = ((area.split(' '))[1][:-1]).split('-')
                if len(area) == 1:
                    area_mid = int(area[0])
                else:
                    area_min = int(area[0])
                    area_max = int(area[1])
                    area_mid = (area_min + area_max) / 2
                cost = int(pri * 10000 / area_mid)
            else:
                cost = pri

            f.write("{},{},{},{}\n".format(name, typ, loc, cost))									# 写入文件
        except Exception as e:
            print(e)
            pass


source_url = 'https://gz.fang.lianjia.com/loupan/pg'
with open(r'lianjia.csv', 'a', encoding='utf-8') as f:
	for i in range(1, 101):
		url = source_url + str(i)						# 构造网址
		print('正在爬取第%d页' % i)						# 打印提示
		try:
			r = requests.get(url)						# 爬取内容
			r.encoding = r.apparent_encoding			# 编码
			html = r.text
			get_data(html, f)
		except:
			pass
	f.close()

	


