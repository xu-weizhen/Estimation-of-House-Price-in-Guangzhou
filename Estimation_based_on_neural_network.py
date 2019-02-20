import tensorflow as tf
import matplotlib.pyplot as plt
import csv
import matplotlib as mpl


# 构造层函数
def add_layer (inputs, in_size, out_size, activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size, out_size]))	# 矩阵
    biases = tf.Variable(tf.zeros([1, out_size])) + 0.1				# 偏置
    Wx_plus_b = tf.add(tf.matmul(inputs, Weights), biases)
    # 根据激活函数处理
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs


times = [560, 580, 600, 620]
tr_loss = []                                    # 训练损失

for time in times:
    x_data = []
    y_data = []

    # 读取数据
    with open('location.csv') as f:
        message = csv.reader(f)
        count = 0											# 数据数量
        for row in message:
            # 选定数据范围
            if row[0] == '0'and float(row[3]) < 24.0:
                # 归一化
                lo = (float(row[2]) - 112) / 2
                la = (float(row[2]) - 22) / 2
                count += 1
                # 分配训练集与测试集
                if count <= time:
                    x_data.append([lo, la])
                    y_data.append([float(row[1])])
    # count=623

    xs = tf.placeholder(tf.float32, [None, 2])
    ys = tf.placeholder(tf.float32, [None, 1])

    # 添加层
    hidden_layer1 = add_layer(xs, 2, 10, activation_function=tf.nn.relu)
    prediction = add_layer(hidden_layer1, 10, 1, activation_function=None)

    # 计算loss
    loss = tf.reduce_mean(tf.abs(ys - prediction))

    # 设置优化器与训练步长
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

    init = tf.global_variables_initializer()		# 初始化
    sess = tf.Session()								# 创建会话
    sess.run(init)

    # 训练
    for i in range(350001):
        sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
        if i % 1000 == 0:
            train_loss = sess.run(loss, feed_dict={xs: x_data, ys: y_data})
            print(i)

    train_loss = sess.run(loss, feed_dict={xs: x_data, ys: y_data})
    tr_loss.append(train_loss)


# 结果可视化
mpl.rcParams['font.sans-serif'] = ['SimHei']    # 图片使其支持中文
plt.plot([560, 580, 600, 620], tr_loss, 'b-', label='Train Loss')
plt.annotate(int(tr_loss[0]), xy=(560, tr_loss[0]), xytext=(560, tr_loss[0] + 20))
plt.annotate(int(tr_loss[1]), xy=(580, tr_loss[1]), xytext=(580, tr_loss[1] + 20))
plt.annotate(int(tr_loss[2]), xy=(600, tr_loss[2]), xytext=(600, tr_loss[2] + 20))
plt.annotate(int(tr_loss[3]), xy=(620, tr_loss[3]), xytext=(620, tr_loss[3] + 20))
plt.legend(loc='best')
plt.xlabel('data')
plt.ylabel('loss')
plt.ylim(tr_loss[3]-100, tr_loss[0]+100)
plt.show()
