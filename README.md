# 广州（及其周边区域）房价分析与估算 #
  
**本项目为入门人工智能时的实践,欢迎指正**  
  
  
## 数据爬取 ##
  
### 数据来源 ###
  
本项目中，房价指广州新房每平方米平均售价，数据来源于链家网（如下图）。在该网站选择广州后，显示的内容除了广州的房子外，还有佛山等周边区域的房子。考虑到这些地区与广州相邻，且与广州之间交通便利，故在分析数据时将其一并考虑。  
![链家网](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/webpage_of_Lianjia.jpg?raw=true)    
  
  
### 爬虫代码 ###
  
Get_information.py  
  
### 说明 ###
  
爬取过程中，发现有的房子给出的价格为全套房的价格，例如下图：  
![单位不一致现象](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/unit_inconsistency.jpg?raw=true)  
对于这类数据，采用的方法是通过其建筑面积，用房子总价除以建筑面积的中位数，得到每平方米的近似价格。  
  
还有一些房子（如下图）的价格显示为“价格待定”，由于这类房子无法进行价格的分析，所以直接舍弃。  
![没有显示价格](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/price_not_shown.jpg?raw=true)  
  
### 代码运行过程 ###
  
程序正常执行过程的部分截图如下：  
![程序正常执行过程](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/process_of_get_information.jpg?raw=true)  
  
### 程序运行结果 ###
  
代码成功运行之后，将数据保存在了文件lianjia.csv中，打开文件，可以看到成功爬取的数据。爬取的内容包括楼盘名、楼盘类型、楼盘位置以及楼盘每平方米均价。  
  
## 数据可视化 ##
  
在进行聚类之前，先将数据可视化，以得到数据的大致分布，以便决定聚类的起始中心。  
  
### 代码 ###
  
Visualization.py  
  
### 运行结果示例 ###
![广州市房价均价可视化结果](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/visualization_of_cluster.png?raw=true)  
  
## 基于房价的聚类 ##
  
### 聚类方法 ###
  
使用K均值（K-means）算法。先手动给出三个聚类的中心点，然后计算各个楼盘房价与中心点的欧式距离，取最小的一个，加入该聚类。然后更新各个聚类的中心点，再重新聚类。重复上述步骤直到中心点不再变化。  
由于K均值聚类算法受到异常点的干扰较大，所以在聚类时，应该避免插入异常点。通过上一节可视化分析可知，房价多集中在0-50000元/㎡之间，所以只传入这一部分的数据。超过50000元/㎡的数据，不参加聚类。并把聚类初始中心设置为10000、30000和50000。
  
### 聚类代码 ###
  
K_Means.py
  
### 运行结果示例 ###
  
聚类中心值变化情况:  
![聚类中心值变化情况](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/central_value_of_cluster.png?raw=true)  
  
各聚类中房屋数量:  
![各聚类中房屋数量](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/Quantity_in_each_cluster.png?raw=true)  
  
聚类结果:  
![各聚类中房屋数量](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/result_of_cluster1.jpg?raw=true) ![各聚类中房屋数量](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/result_of_cluster2.jpg?raw=true)  
  
## 基于距离的房价估算 ##
  
因为商业类楼房较少，且一般购买住宅不会考虑购买商业类楼房，所以只对住宅和别墅进行房价估计。  
为获取房子所在的经纬度，利用高德地图进行查询。  
  
![高德页面](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/webpage_of_Gaode.jpg?raw=true)  
  
### 获取房子经纬度代码 ###
  
Get_latitude_and_longitude.py  
  
### 说明 ###
  
在进行小规模的爬取时，发现提交相同数量的房子地址之后，在多次运行时，成功得到的结果数量有所不同。因为不能断定是高德地图页面不稳定还是其他原因，所以在代码中添加了失败列表，把爬取失败的房子地点保存在该列表中。并在之后对该列表中的数据进行重新爬取，以获得更多的数据。同时，发现在爬取了一定数量的数据之后，高德地图页面会出现需要拖动拼图进行验证的验证框。所以在对失败列表中的数据进行重新爬取之前，设置了一定的休眠时间，使得有时间可以人工完成验证，保证程序可以继续正常运行。  
  
### 代码正确运行过程 ###
 
![代码正确运行过程](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/process_of_get_longitude_and_latitude.jpg?raw=true)  
  
### 代码运行结果 ###
  
代码运行之后，将数据保存在了文件location.csv中。第一列为房屋类型，0为住宅，1位别墅；第二列为每平方米价格；第三列为经度；第四列为纬度。  
  
在对文件中的数据进行浏览后发现，别墅类信息较少，分布距离较远。因此，为了提高估算的准确性，只对住宅价格进行估算。  
  
### 房价估算代码 ###
  
Distance-based_estimation.py  
  
### 说明 ###
  
平均预测价格通过取距离最近的三个已知价格的楼盘的每平方价格的平均值，估算目标楼盘价格。  
带权预测价格通过距离最近的三个已知价格楼盘的每平方价格，对目标楼盘价格进行估计。已知价格楼盘的距离与权重示意图如下：  
![距离与权重示意图](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/distance_and_weight.jpg?raw=true)   
  
得到公式如下：  
![公式](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/weight_formula.jpg?raw=true)  
  
### 运行结果示例 ###
    
![房价估算结果](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/estimation_result.jpg?raw=true) 
  
  
## 基于神经网络的房价估计 ##
  
通过神经网络，可以构建广州及周边地区的房价曲面，进而实现对房价的估计。  
  
### 网络模型 ###
  
本次实验使用三层网络，结构如下图所示。其中输入层有两个神经元，代表输入的经度和纬度。隐藏层有一层，包含10个神经元。输出层有一个神经元，为预测的价格。  
![神经网络结构](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/neural_network_architecture.jpg?raw=true)  
  
### 代码 ###

Estimation_based_on_neural_network.py  
  
### 说明 ###
  
运行之后得到的模型误差较大，无法达到估算房价的要求。  
在进行调整训练步长、网络结构等尝试之后，损失仍然基本不变。  
而在改变训练集大小之后，发现损失有所变化，随着训练集数据的增加，训练之后的损失有所减低。loss随训练集数量变化曲线如下图。由此可以推测，当数据数量达到一定数量之后，将可以训练出损失足够小、满足需要的模型。 
![loss随训练集数量变化曲线](https://github.com/xu-weizhen/Estimation-of-House-Price-in-Guangzhou/blob/master/picture/changes_in_losses.png?raw=true)  
   
因为房价波动影响因素复杂，难以用历史房价衡量当前房价，且当前在售的楼盘数量有限，故难以获得大量的数据对网络进行训练。因此，利用神经网络对新房价格进行估算有较大的难度。  
