import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
# 数据读取+预处理
data = pd.read_excel("Gender.xlsx")
gender = np.array(data['gender'].tolist())
ppl_info = []
for x, y in zip(data["Height"], data["Weight"]):
    ppl_info.append([round(x, 2), round(y, 2)])
ppl_info = np.array(ppl_info)
# 算法核心


def KNN(test, x_labels, y_labels, k):
    x_labels_size = x_labels.shape[0]
    distance = (np.tile(test, (x_labels_size, 1)) -
                x_labels)**2  # 先计算对应x,y下标相减的平方
    ad_distances = distance.sum(axis=1)
    sq_distances = ad_distances ** 0.5  # 计算有根号的欧式距离
    ed_distances = sq_distances.argsort()  # 对欧式距离进行索引升序排序，方便下面调用字典
    classdict = {}
    for i in range(k):  # k个临近点中，哪个类型多就归为哪类
        voteI_label = y_labels[ed_distances[i]]
        classdict[voteI_label] = classdict.get(
            voteI_label, 0) + 1  # 对于分类结果进行对应计数，get函数：返回0或者搜索值
    sort_classdict = sorted(
        classdict.items(), key=operator.itemgetter(1), reverse=True)
    return sort_classdict[0][0]


KNN([180, 75], ppl_info, gender, 3)
# The dataset I designed is based on the average height and weight of male and female in China
# This KNN model aims to input a testing data and recognize it as male or female
