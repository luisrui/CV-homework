#Average-linkage算法
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
#数据预处理
x1,y1,x2,y2,x3,y3 = [],[],[],[],[],[]
set_cluster_train_number = 100#自己定样本点
threshold = 7 #自己定阈值
for i in range(set_cluster_train_number):
    x1.append(random.uniform(0,10))
    y1.append(random.uniform(0,3))
    x2.append(random.uniform(20,30))
    y2.append(random.uniform(6,8))
for i in range(int(set_cluster_train_number/5)):
    x3.append(random.uniform(10,20))
    y3.append(random.uniform(3,6))
pot_x,pot_y= x1+x2+x3,y1+y2+y3
#封装聚类
class cluster:
    #这里的x,y都是列表，存储的是一个聚类中的xy值
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.length = len(self.x)
#计算欧拉距离
def eular_distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2) 

def aLink(cluster1,cluster2):
    overall = 0
    for x1,y1 in zip(cluster1.x,cluster1.y):
        for x2,y2 in zip(cluster2.x,cluster2.y):
            overall += eular_distance(x1,y1,x2,y2)
    return overall / (cluster1.length*cluster2.length)

def sLink(cluster1,cluster2):
    overall = 100000
    for x1,y1 in zip(cluster1.x,cluster1.y):
        for x2,y2 in zip(cluster2.x,cluster2.y):
            overall = min(overall,eular_distance(x1,y1,x2,y2))
    return overall

def cLink(cluster1,cluster2):
    overall = -100000
    for x1,y1 in zip(cluster1.x,cluster1.y):
        for x2,y2 in zip(cluster2.x,cluster2.y):
            overall = max(overall,eular_distance(x1,y1,x2,y2))
    return overall

#利用并查集把元素融合到一起
clusters = []
united_length = [0]
for single_x,single_y in zip(pot_x,pot_y):
    clusters.append(cluster([single_x],[single_y]))

def find(number,united):
    if united[number] == number:
        return number
    else:
        return find(united[number],united)
    
def merge(son,father,united):
    united[find(son,united)] = find(father,united)


while True:
    united = [i for i in range(len(clusters))]
    if len(united) == united_length[len(united_length)-1]:
        break
    else:
        united_length.append(len(united))                          
    for i in range(len(clusters)):
        for j in range(i+1,len(clusters)):
            if aLink(clusters[i],clusters[j]) <= threshold:
                merge(j,i,united)
    count = 0
    appear_number = []
    new_clusters = []
    for i in range(len(clusters)):
        if united[i] in appear_number:
            continue
        else:
            count = united[i]
            appear_number.append(count)
            for j in range(i+1,len(united)):
                if united[i] == united[j]:
                    clusters[i].x += clusters[j].x
                    clusters[i].y += clusters[j].y
            new_clusters.append(clusters[i])
    clusters = new_clusters
plot = [[] for i in range(len(clusters))]
for clu in clusters:
    plot[i] = plt.plot(clu.x,clu.y,".")
plt.show()