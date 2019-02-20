import csv
import math

li = []                                         # 原始数据

# 读取元素数据
with open('location.csv') as f:
    message = csv.reader(f)
    count = 0
    for row in message:
        count += 1
        if count > 5:
            li.append(row)

addr = input("输入经纬度：")
try:
    longtitude = float(addr.split(' ')[0])
    latitude = float(addr.split(' ')[1])
except:
    print("输入数据有误")
    exit(1)

min_list = []                           # 最近房子列表
count = 0                               # 已保存最近房子数
for row in li:
    # 只考虑住宅
    if row[0] == '0':
        # 前三条数据直接放入列表
        if count < 3:
            dis = math.sqrt(pow((longtitude-float(row[2])), 2) + pow((latitude-float(row[3])), 2))
            min_list.append((int(row[1]), dis))
            count += 1
        else:
            # 将距离最远房子放到列表最后
            if min_list[0][1] > min_list[2][1]:
                t = min_list[0]
                min_list[0] = min_list[2]
                min_list[2] = t
            if min_list[1][1] > min_list[2][1]:
                t = min_list[1]
                min_list[1] = min_list[2]
                min_list[2] = t

            # 计算距离
            dis = math.sqrt(pow((longtitude - float(row[2])), 2) + pow((latitude - float(row[3])), 2))

            # 判断是否放入列表
            if dis < min_list[2][0]:
                min_list[2] = (int(row[1]), dis)

# 与已知价格房子距离过近，直接取已知房子价格
if min_list[0][1] < 1e-4:
    cost = min_list[0][0]
elif min_list[1][1] < 1e-4:
    cost = min_list[1][0]
elif min_list[2][1] < 1e-4:
    cost = min_list[2][0]
else:
    # 计算权重
    w1 = 1.0 / ((min_list[0][1] / min_list[1][1]) + (min_list[0][1] / min_list[2][1]) + 1)
    w2 = (min_list[0][1] / min_list[1][1]) * w1
    w3 = (min_list[0][1] / min_list[2][1]) * w1
    cost = int(w1 * min_list[0][0] + w2 * min_list[1][0] + w3 * min_list[2][0])
print("带权预测价格为：%d元/㎡" % cost)               # 打印结果

# 计算平均预测价格
sum_d = min_list[0][0] + min_list[1][0] + min_list[2][0]
w1 = min_list[0][0]/sum_d
w2 = min_list[1][0]/sum_d
w3 = min_list[2][0]/sum_d
cost = int(w1*min_list[0][0] + w2*min_list[1][0] + w3*min_list[2][0])
cost = int((min_list[0][0] + min_list[1][0] + min_list[2][0])/3)
print("平均预测价格为：%d元/㎡" % cost)               # 打印结果

