import csv
import urllib.request
import time

li = []
url = "https://restapi.amap.com/v3/place/text?s=rsv3&children=&key=8325164e247e15eea68b59e89200988b&page=1&offset=10&city=440100&language=zh_cn&callback=jsonp_314777_&platform=JS&logversion=2.0&sdkversion=1.3&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker&csid=8D774204-8B63-4D57-861B-49D974D36E91&keywords=%E4%BB%8E%E5%8C%96%E4%BB%8E%E5%8C%96%E6%B1%9F%E5%9F%94%E8%A1%97%E6%B1%9F%E6%9D%91%E5%9C%B0%E6%AE%B5"

# 读入文件内容
with open('lianjia.csv') as f:
    message = csv.reader(f)
    for i, row in enumerate(message):
        if i > 0:
            li.append(row)

li_sum = len(li)						# 数据数量
print('共有%d个地址待查询' % li_sum)	# 打印提示信息


with open(r'location.csv', 'a', encoding='utf-8') as f:
    ti = 1                             # 循环次数
    count = 0                          # 成功个数
    shop = 0
    fail_list = []                     # 失败列表
    while len(li) > 0 and ti <= 5:
        for i in li:
            try:
                # 获得房子类别
                if i[1][0] == '住':
                    typ = 0             # 住宅
                elif i[1][0] == '别':
                    typ = 1             # 别墅
                else:
                    shop += 1
                    continue

                data = {}
                data['s'] = 'rsv3'
                data['children'] = None
                data['key'] = '8325164e247e15eea68b59e89200988b'
                data['page'] = '1'
                data['offset'] = '10'
                data['city'] = '440100'
                data['language'] = 'zh_cn'
                data['callback'] = 'jsonp_522677_'
                data['platform'] = 'JS'
                data['logversion'] = '2.0'
                data['sdkversion'] = '1.3'
                data['appname'] = 'https://lbs.amap.com/console/show/picker'
                data['csid'] = '55D7AAAB-329D-4486-B869-7811BA56D7AB'
                data['keywords'] = i[2]                         # 写入地址
                data = urllib.parse.urlencode(data).encode('utf-8')
                response = urllib.request.urlopen(url, data)    # 提交查询
                html = response.read().decode('utf-8')          # 查询结果

                # 获得经纬度
                if len(html) == 5470:
                    tude = ((((html.split(':'))[15]).split('"'))[1]).split(',')
                    longitude = tude[0]
                    latitude = tude[1]
                    f.write("{},{},{},{}\n".format(typ, i[3], longitude, latitude))
                    count += 1  # 成功个数加一
                else:
                    tude = ((((html.split(':'))[16]).split('"'))[1]).split(',')
                    longitude = float(tude[0])
                    latitude = float(tude[1])

                # 写入表格
                f.write("{},{},{},{}\n".format(typ, i[3], longitude, latitude))

                count += 1              # 成功个数加一

                # 输出提示
                if count % 20 == 0:
                    print('已查询成功%d个地址' % count)
            except :
                fail_list.append(i)  # 加入失败列表

        li = fail_list
        fail_list = []
        time.sleep(5)
        print("已完成%d次" % ti)
        ti += 1

print('查询成功%d个' % count)
print('查询失败%d个' % (li_sum - count - shop))