import csv
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']    # 图片使其支持中文

def k_means(clusterNum, centers, data):
    
    change = True                               # 聚类中心是否发生改变

    clusters = [[] for _ in range(clusterNum)]
    centerList = []
    for center in centers:
        centerList.append([center])

    # 计算初始所在聚类
    for row in data:
        distance = []                               # 与每个类的中心的距离
        for center in centers:
            distance.append(abs(row[1] - center))   # 计算与每个类中心的距离，并保存

        minDis = distance.index(min(distance))      # 获得距离最近的类的索引
        clusters[minDis].append(row)                # 将该点放入距离最近的类

    while change:

        # 计算聚类中心
        for i in range(len(centers)):       # 对每个聚类进行更新
            s = 0                           # 该聚类中房价总和
            for item in clusters[i]:
                s += item[1]
            s = int(s / len(clusters[i]))   # 该聚类中房价平均值

            centers[i] = s                  # 更新聚类中心
            centerList[i].append(s)

        change = False                      # 聚类中心已改变

        # 处理类中数据
        for i in range(clusterNum):                 # 对每个聚类中的数据进行处理
            delList = []                            # 需要移出该聚类的数据的索引
            for j, item in enumerate(clusters[i]):
                distance = []                       # 保存该数据与每个聚类中心的距离
                for center in centers:
                    distance.append(abs(item[1] - center))  # 计算与聚类中心距离

                minDis = distance.index(min(distance))      # 获得距离最近的聚类中心
                if minDis != i:                     # 判断距离最近的聚类中心是否发生变化
                    change = True
                    clusters[minDis].append(row)    # 将该数据加入距离最近的聚类中心所在的聚类
                    delList.append(j)               # 记录该数据在本聚类中索引

            delList.sort(reverse=True)              # 将待删除的数据索引逆序排序
            for index in delList:
                del clusters[i][index]              # 删除已经移出该聚类的数据
                

    time = len(centerList[0])                       # 聚类中心更新次数
    timeList = []
    for i in range(0, time):
        timeList.append(i)                          # x轴坐标值

    # 绘制聚类中心值变化曲线
    color = ['r','g', 'b', 'y', 'm']

    for i, l in enumerate(centerList):
        plt.plot(timeList, l, c=color[i % 5])

    plt.ylim(bottom=5000)
    plt.title("中心值变化情况")
    plt.xlabel('聚类次数')
    plt.ylabel('中心价格')

    plt.plot([time - 1, time - 1], [0, centerList[-1][-1]], 'k:', linewidth=0.8)

    for i, l in enumerate(centerList):
        plt.scatter(time - 1, l[-1], s=20, color=color[i % 5])
        plt.annotate(l[-1], xy=(time - 1, l[-1]), xytext=(time - 1, l[-1] + 1000))

    plt.show()

    # 绘制聚类中元素个数柱状图
    nameList = [i + 1 for i in range(clusterNum)]
    numList = [len(c) for c in clusters]
    plt.ylim(top=550)
    plt.ylabel("数量")  # y轴标签
    plt.xlabel("聚类")
    for x, y in zip(nameList, numList):
        plt.text(x, y + 5, y, ha='center')
    plt.bar(nameList, numList, width=0.6, facecolor='#9999ff')
    labelList = ['聚类' + str(i + 1) for i in range(clusterNum)]
    plt.xticks(nameList, labelList)
    plt.show()

    # 各聚类中包含的地点及次数
    count = [{} for i in range(clusterNum)]

    for i, cluster in enumerate(clusters):
        for item in cluster:
            if item[0] in count[i]:
                count[i][item[0]] += 1
            else:
                count[i][item[0]] = 1

    # 对同时存在于两个聚类中的地点，只保留在次数较多的聚类中
    for i in range(len(count)):
        delList = []
        for item in count[i].keys():
            for j in range(len(count)):
                if i != j and item in count[j]:
                    if count[j][item] > count[i][item]:
                        delList.append(item)
                    else:
                        del count[j][item]
        for item in set(delList):
            del count[i][item]
                    
    # 输出次数超过5的结果
    for i in range(clusterNum):
        print('\n聚类' + str(i + 1) + ':')
        for key in count[i].keys():
            if count[i][key] >= 5:
                print(key, end='  ')
        print()


data = []                                       # 处理后数据

# 读取元素数据
with open('data.csv', encoding='utf-8') as f:
    message = csv.reader(f)
    for row in message:
        if row[1][0] == '住':
            try:
                price = int(row[3])

                if price <= 150000:
                    addr = row[2].split(' ')

                    t = [addr[0], price]
                    data.append(t)
            except:
                continue

clusterNum = 3
centers = [15000, 35000, 55000]

k_means(clusterNum, centers, data)