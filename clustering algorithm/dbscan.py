#DBSCAN算法 基于密度的空间聚类算法
import pandas as pd
import matplotlib.pyplot as plt
import random
import math
#数据预处理
df = pd.DataFrame(pd.read_csv("/Users/cairui/CV-homework/clustering algorithm/data/clusterData1.10k.dat",header=None))
pot_x,pot_y= [],[]
for i in range(len(df[0])):
    temp = df[0][i].split(" ")
    pot_x.append(float(temp[0]))
    pot_y.append(float(temp[1]))
#DBSCAN算法
#先定义每个点的三个状态
noise = -1
unmarked = 0
core = 1
#封装点类
class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = unmarked
    
    #定义点在半径圆内
    def within(self,new_point,radius):
        if eular_distance(self,new_point) <= radius:
            return True
        else:
            return False
#封装聚类
class cluster:
    #这里的x,y都是列表，存储的是一个聚类中的xy值
    def __init__(self,p):
        self.points=[p]
        self.length = len(self.points)
    
    def add(self,p):
        self.points.append(p)
        self.length += 1
    
    def getX(self):
        x = []
        for p in self.points:
            x.append(p.x)
        return x
    
    def getY(self):
        y = []
        for p in self.points:
            y.append(p.y)
        return y
points = []#保存所有点类
for x1,y1 in zip(pot_x,pot_y):
    points.append(point(x1,y1))

#计算欧拉距离
def eular_distance(point1:point,point2:point):
    return math.sqrt((point1.x-point2.x)**2+(point1.y-point2.y)**2) 


#算法核心
radius = 30
clusters = []#保存所有聚类

for p_center in points:
    if p_center.state == unmarked:
        new_cluster = [p_center]
        for p in points:
            if (p != p_center) & (p_center.within(p,radius)):
                p.state = core
                new_cluster.append(p_center)
        if len(new_cluster) == 1:
            p_center.state = noise

for p_center in points:
    if p_center.state == unmarked & p_center.state != noise:
        new_cluster = [p_center]
        for p in points:
            if (p != p_center) & (p_center.within(p,radius)):
                p.state = core
                new_cluster.append(p)
        p_center.state = core
        for new_p in new_cluster:
            if new_p != p_center:
                for p_expand in points:
                    if (p_expand not in new_cluster) & (p_expand.state == unmarked) & (new_p.within(p_expand,radius)):
                        p_expand.state = core
                        new_cluster.append(p_expand)
        clusters.append(new_cluster)
for p in points:
    if p.state == noise:
        clusters.append([p])
plot = [[] for i in range(len(clusters))]
for i in range(len(clusters)):
    x,y = [],[]
    for j in range(len(clusters[i])):
        x.append(clusters[i][j].x)
        y.append(clusters[i][j].y)
    plot[i] = plt.plot(x,y,".")
plt.show()