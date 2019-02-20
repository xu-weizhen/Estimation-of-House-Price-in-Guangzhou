import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
import random

mpl.rcParams['font.sans-serif'] = ['SimHei']    # 图片使其支持中文
original_li = []                                # 元素数据
li = []                                         # 处理后数据
count = -1                                      # 计数
max_price = -1                                  # 最低价
max_price_index = -1                            # 最低价所在处
min_price = 9999999                             # 最高价
max_price_index = -1                            # 最高价所在处
loc = []                                        # 房子地点列表

# 读取元素数据
with open('lianjia.csv') as f:
    message = csv.reader(f)
    for i, row in enumerate(message):
        original_li.append(row)


for m in original_li:
    try:
        # 获取价格
        cost = int(m[3])

        # 获取房子所在地
        addr = m[2].split(' ')
        addr = addr[0]
        loc.append(addr)                # 加入房子地点列表

        # 获取房子类型
        t = m[1]
        if t[0] == '住':
            typ = 0                     # 住宅
        elif t[0] == '别':
            typ = 1                     # 别墅
        else:
            typ = 2                     # 商业

        t = [typ, addr, cost]           # 组成列表
        li.append(t)                    # 加入列表
        count += 1                      # 计数加一

        # 计数最大价格
        if cost > max_price:
            max_price = cost
            max_price_index = count

        # 计数最小价格
        if cost < min_price:
            min_price = cost
            min_price_index = count
    except:
        pass

del original_li                         # 将元素数据从内存中删除

# 住宅点列表
residence_x = []
residence_y = []
residence_c = []

# 别墅点列表
villa_x = []
villa_y = []
villa_c = []

# 商业点列表
business_x = []
business_y = []
business_c = []

loc = list(set(loc))                        # 删除重复地点

# 颜色列表
color_list = ['#A9A9A9', '#800000', '#FF0000', '#FF6347', '#D2B48C', '#FFA500', '#FFD700', '#FFFF00', '#808000', '#7CFC00', '#008000', '#00FF7F', '#00FFFF', '#00BFFF', '#0000FF', '#8A2BE2', '#800080', '#FFB6C1', '#000000',  '#D2691E']

count = 0
for row in li:
    count += 1
    index = loc.index((row[1].split(' '))[0])   # 房子所在地点索引

    # 将房子价格加入相应列表
    if count % 10 == 0:
        if row[0] == 0:
            residence_x.append(row[2])
            residence_y.append(random.randint(5, 31))
            residence_c.append(color_list[index])
        elif row[0] == 1:
            villa_x.append(row[2])
            villa_y.append(random.randint(35, 61))
            villa_c.append(color_list[index])
        elif row[0] == 2:
            business_x.append(row[2])
            business_y.append(random.randint(65, 91))
            business_c.append(color_list[index])

# 绘制散点图
plt.scatter(residence_x, residence_y, c=residence_c, marker='o', label='住宅')
plt.scatter(villa_x, villa_y, c=villa_c, marker='s', label='别墅')
plt.scatter(business_x, business_y, c=business_c, marker='^', label='商业')
plt.legend(loc='best')                  # 设置标签
plt.title("广州市房价均价(元/㎡)")      # 设置标题
plt.yticks(())                          # 不显示y轴数值
plt.show()                              # 显示图像

