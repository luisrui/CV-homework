# Support Vector Mechine
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(8)  # 保证随机的唯一性
N = 20
array = np.random.randn(N, 2)
x = np.r_[array-[3, 3], array+[3, 3]]
y = np.array([-1]*N+[1]*N)
N,M = x.shape
C=100
alpha = np.ones(N)
b = 0.0
max_iter = 10
def K(i,j):#高斯核函数
    l2 = np.linalg.norm(x[i]-x[j],ord=2)
    return np.exp(-l2/200)
def g(i):#预测函数
    _sum = 0
    for j in range(N):
        _sum += alpha[j]*y[j]*K(i,j)
    _sum += b
    return _sum
def E(i): #误差函数
    return g(i)-y[i]
#KKT条件
def kkt(i):
    if alpha[i] == 0:
        return y[i] * g(i) >= 1
    if alpha[i] == C:
        return y[i] * g(i) <= 1
    if 0 < alpha[i] < C:
        return y[i] * g(i) == 1
    return False
#获得KKT条件带来的错误
def get_kkt_difference(i):
    if kkt(i):
        return 0
    if alpha[i] == 0:
        return 1 - y[i] * g(i)
    if alpha[i] == C:
        return y[i] * g(i) - 1
    if 0 < alpha[i] < C:
        return np.abs(1-y[i] * g(i))
    return 100

def pick_idx():
    #寻找违反kkt最严重数据点
    max_kkt_difference = 0
    _i = -1
    for i in range(N):
        if kkt(i):
            continue
        temp = max_kkt_difference
        max_kkt_difference = max(max_kkt_difference, get_kkt_difference(i))
        if temp != max_kkt_difference:
            _i = i
    #寻找对于_i误差最大的数据点
    max_E_difference = 0
    _j = -1
    for i in range(N):
        E_difference = np.abs(E(_i)-E(i))
        temp = max_E_difference 
        max_E_difference = max(max_E_difference, E_difference)
        if temp != max_E_difference:
            _j = i
    return _i,_j
def get_L_and_H(i,j):
    L,H = 0,0
    if y[i] != y[j]:
        L = max(0,alpha[j]-alpha[i])
        H = min(C,C+alpha[j]-alpha[i])
    else:
        L = max(0,alpha[j] + alpha[i] - C)
        H = max(C,alpha[j] + alpha[i])
    return L,H
def get_b(i,j,alpha_new_i,alpha_new_j):
    b1 = 0-E(i)-y[i]*K(i,i)*(alpha_new_i-alpha[i]) -y[j]*K(j,i)*(alpha_new_j-alpha[j])+b
    b2 = 0-E(j)-y[i]*K(i,j)*(alpha_new_i-alpha[i]) -y[j]*K(j,j)*(alpha_new_j-alpha[j])+b
    if 0 < alpha_new_i < C and 0 < alpha_new_j < C:
        return b1
    return (b1+b2)/2
def get_new_alpha(i,j,L,H):
    alpha_new_j = alpha[j] + y[j] * (E(i)-E(j)) / (K(i,i)+K(j,j)-2*K(i,j))
    if alpha_new_j > H:
        alpha_new_j = H
    if alpha_new_j < L:
        alpha_new_j = L
    alpha_new_i = alpha[i] + y[i]*y[j]*(alpha[j]-alpha_new_j)
    return alpha_new_i,alpha_new_j
def get_w():
    return np.dot(alpha * y, x)
def train():
    global alpha
    global b
    iterStep = 0
    while(iterStep < max_iter):
        iterStep += 1
        i, j = pick_idx()
        L, H = get_L_and_H(i,j)
        alpha_new_i, alpha_new_j = get_new_alpha(i,j,L,H)
        b = get_b(i,j,alpha_new_i,alpha_new_j)
        alpha[i] = alpha_new_i
        alpha[j] = alpha_new_j
train()
w = get_w()
x_divide = [i for i in range(-20,20)]
y_divide = []
for _x in x_divide:
    _y = (0 - b - _x*w[0])/ w[1]
    y_divide.append(_y)
x1,y1=[s[0] for s in x],[s[1] for s in x]
plot1 = plt.plot(x1,y1,'.')
plot2 = plt.plot(x_divide,y_divide)
plt.plot()
