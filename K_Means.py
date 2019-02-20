import csv
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']    # 图片使其支持中文
li = []                                         # 原始数据
m_li = []                                       # 处理后数据

# 读取元素数据
with open('lianjia.csv') as f:
    message = csv.reader(f)
    for i, row in enumerate(message):
            li.append(row)

# 处理元素数据
for row in li:
    try:
        price = int(row[3])

        if price <= 100000:
            addr = row[2].split(' ')

            t = [row[1], addr[0], price]
            m_li.append(t)
    except:
        continue

del li                              # 删除内存中的元素数据
center1 = 10000                     # 聚类1中心
center2 = 25000                     # 聚类2中心
center3 = 40000                     # 聚类3中心
change = True                       # 聚类中心是否发生改变
cluster1 = []                       # 聚类1内容
cluster2 = []                       # 聚类2内容
cluster3 = []                       # 聚类3内容
center1_list = [center1]            # 聚类1中心历史值
center2_list = [center2]            # 聚类2中心历史值
center3_list = [center3]            # 聚类3中心历史值

for m in m_li:
    # 计算初始所在聚类
    distance = [abs(m[2] - center1), abs(m[2] - center2), abs(m[2] - center3)]
    min_dis = distance.index(min(distance))
    if min_dis == 0:
        cluster1.append(m)
    elif min_dis == 1:
        cluster2.append(m)
    else:
        cluster3.append(m)

while change:
    # 计算聚类中心
    sum_c = 0
    for c1 in cluster1:
        sum_c += c1[2]
    center1 = int(sum_c / len(cluster1))

    sum_c = 0
    for c2 in cluster2:
        sum_c += c2[2]
    center2 = int(sum_c / len(cluster2))

    sum_c = 0
    for c3 in cluster3:
        sum_c += c3[2]
    center3 = int(sum_c / len(cluster3))

    # 添加入聚类中心历史值列表
    center1_list.append(center1)
    center2_list.append(center2)
    center3_list.append(center3)

    change = False                  # 聚类中心已改变

    # 处理第一类中数据
    count = 0
    del_list = []
    for c1 in cluster1:
        if abs(c1[2] - center2) < abs(c1[2] - center1):
            change = True
            cluster2.append(c1)
            del_list.append(count)
        elif abs(c1[2] - center3) < abs(c1[2] - center1):
            change = True
            cluster3.append(c1)
            del_list.append(count)
        count += 1
    del_list.sort()
    del_list.reverse()
    for i in del_list:
        del cluster1[i]

    # 处理第二类中数据
    count = 0
    del_list = []
    for c2 in cluster2:
        if abs(c2[2] - center1) < abs(c2[2] - center2):
            change = True
            cluster1.append(c2)
            del_list.append(count)
        elif abs(c2[2] - center3) < abs(c2[2] - center2):
            change = True
            cluster3.append(c2)
            del_list.append(count)
        count += 1
    del_list.sort()
    del_list.reverse()
    for i in del_list:
        del cluster2[i]

    # 处理第三类中数据
    count = 0
    del_list = []
    for c3 in cluster3:
        if abs(c3[2] - center1) < abs(c3[2] - center3):
            change = True
            cluster1.append(c3)
            del_list.append(count)
        elif abs(c3[2] - center2) < abs(c3[2] - center3):
            change = True
            cluster2.append(c3)
            del_list.append(count)
        count += 1
    del_list.sort()
    del_list.reverse()
    for i in del_list:
        del cluster3[i]

time = len(center1_list)        # 聚类中心更新次数
time_list = []
for i in range(0, time):
    time_list.append(i)         # x轴坐标值

# 绘制聚类中心值变化曲线
plt.plot(time_list, center1_list, c='r')
plt.plot(time_list, center2_list, c='g')
plt.plot(time_list, center3_list, c='b')
plt.ylim(bottom=5000)
plt.title("中心值变化情况")
plt.xlabel('聚类次数')
plt.ylabel('中心价格')
plt.plot([time - 1, time - 1], [0, center3_list[-1]], 'k:', linewidth=0.8)
plt.scatter(time - 1, center1_list[-1], s=20, color='r')
plt.scatter(time - 1, center2_list[-1], s=20, color='g')
plt.scatter(time - 1, center3_list[-1], s=20, color='b')
plt.annotate(center1_list[-1], xy=(time - 1, center1_list[-1]), xytext=(time - 1, center1_list[-1] + 1000))
plt.annotate(center2_list[-1], xy=(time - 1, center2_list[-1]), xytext=(time - 1, center2_list[-1] + 1000))
plt.annotate(center3_list[-1], xy=(time - 1, center3_list[-1]), xytext=(time - 1, center3_list[-1] + 1000))
plt.show()

# 绘制聚类中元素个数柱状图
name_list = [1, 2, 3]
num_list = [len(cluster1), len(cluster2), len(cluster3)]
plt.ylim(top=550)
plt.ylabel("数量")  # y轴标签
plt.xlabel("聚类")
for x, y in zip(name_list, num_list):
    plt.text(x, y + 5, y, ha='center')
plt.bar(name_list, num_list, width=0.6, facecolor='#9999ff')
plt.xticks((1, 2, 3), ('聚类1', '聚类2', '聚类3'))
plt.show()

# 各聚类中包含的地点及次数
loc1 = {}
loc3 = {}
loc2 = {}
for c1 in cluster1:
    if c1[0][0] == '商' or c1[0][1] == '商' or c1[0][0] == '写':
        c1[0] = '商业类'
    s = c1[1] + ' ' + c1[0]
    if s in loc1:
        loc1[s] += 1
    else:
        loc1[s] = 1

for c2 in cluster2:
    if c2[0][0] == '商' or c2[0][1] == '商' or c2[0][0] == '写':
        c2[0] = '商业类'
    s = c2[1] + ' ' + c2[0]
    if s in loc2:
        loc2[s] += 1
    else:
        loc2[s] = 1

for c3 in cluster3:
    if c3[0][0] == '商' or c3[0][1] == '商' or c3[0][0] == '写':
        c3[0] = '商业类'
    s = c3[1] + ' ' + c3[0]
    if s in loc3:
        loc3[s] += 1
    else:
        loc3[s] = 1

# 对同时存在于两个聚类中的地点，只保留在次数较多的聚类中
del_list1 = []
del_list2 = []
del_list3 = []
for c1 in loc1:
    if c1 in loc2:
        if loc2[c1] > loc1[c1]:
            del_list1.append(c1)
        else:
            del loc2[c1]
            if c1 in loc3:
                if loc3[c1] > loc1[c1]:
                    del_list1.append(c1)
                else:
                    del loc3[c1]
for de in del_list1:
    del loc1[de]

for c2 in loc2:
    if c2 in loc3:
        if loc2[c2] > loc3[c2]:
            del loc3[c2]
        else:
            del_list2.append(c2)
for de in del_list2:
    del loc2[de]

# 输出次数超过5的结果
print('\n聚类1:')
for result in loc1:
    if loc1[result] >= 5:
        print(result)

print('\n聚类2:')
for result in loc2:
    if loc2[result] >= 5:
        print(result)

print('\n聚类3:')
for result in loc3:
    if loc3[result] >= 5:
        print(result)

