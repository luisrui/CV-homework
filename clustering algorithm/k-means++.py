#二维聚类的K-means算法及优化
import pandas as pd
import matplotlib.pyplot as plt
import random
#数据预处理
df = pd.DataFrame(pd.read_csv("/Users/cairui/CV-homework/clustering algorithm/data/clusterData2.8k.dat",header=None))
pot_x,pot_y= [],[]
for i in range(len(df[0])):
    temp = df[0][i].split(" ")
    pot_x.append(float(temp[0]))
    pot_y.append(float(temp[1]))
#实现K-Means初始化优化K-Means++
rdm = random.randint(0,len(df)-1)
centers_x = [pot_x[rdm]]
centers_y = [pot_y[rdm]]
def choose_center(pot_x,pot_y,centers_x,centers_y,k):
    #通过训练选择优化的初始聚类中心
    max_x,max_y,max_distance = 0,0,0;
    for i in range(k-1):
        for x,y in zip(pot_x,pot_y): 
            for centerx,centery in zip(centers_x,centers_y):
                temp = max_distance
                distance = (x-centerx)**2+(y-centery)**2
                max_distance = max(max_distance,distance)
                if(temp!=max_distance):
                    max_x = x
                    max_y = y
        centers_x.append(max_x)
        centers_y.append(max_y)
    return centers_x,centers_y
centers_x,centers_y = choose_center(pot_x,pot_y,centers_x,centers_y,3)
#传统的k-means算法
flag = True
clusters_x,clusters_y=[[] for i in range(len(centers_x))],[[] for i in range(len(centers_y))]
while(flag):
    clusters_x,clusters_y=[[] for i in range(len(centers_x))],[[] for i in range(len(centers_y))]
    for x,y in zip(pot_x,pot_y):
        min_distance = 1000000
        min_index = 0
        for i in range(len(centers_x)):
            temp = min_distance
            distance = (x-centers_x[i])**2+(y-centers_y[i])**2
            min_distance = min(distance,min_distance)
            if min_distance != temp:
                min_index = i
        clusters_x[min_index].append(x)
        clusters_y[min_index].append(y)
    new_center_x,new_center_y = [],[]
    for cluster_x,cluster_y in zip(clusters_x,clusters_y):
        new_x = sum(cluster_x)/len(cluster_x)
        new_y = sum(cluster_y)/len(cluster_y)
        new_center_x.append(new_x)
        new_center_y.append(new_y)
    distance = 0
    for i in range(len(centers_x)):
        distance +=(centers_x[i]-new_center_x[i])**2+(centers_y[i]-new_center_y[i])**2
    if distance <=10e-4:
        flag = False
    centers_x,centers_y = new_center_x,new_center_y
plot = [[] for i in range(len(clusters_x))]
for cluster_x, cluster_y in zip(clusters_x,clusters_y):
    plot[i] = plt.plot(cluster_x,cluster_y,"x")
plt.show()