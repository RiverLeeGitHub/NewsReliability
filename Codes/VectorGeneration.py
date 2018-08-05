# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 21:51:15 2018
向量生成
@author: lijiang
"""

#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
import numpy as np
import math
import time


#向量之间的语义相似度
# sim=np.array(
#     [[1,0.3,0.4,0.2],
#      [0.3,1,0.5,0.3],
#      [0.4,0.5,1,0.5],
#      [0.2,0.3,0.5,1]])
# sim=SentenceSimilarity.similarity()

vector=[]
current_angle=[]
aim_angle=[]

def count_angle(sim):
    global aim_angle
    ##计算向量之间的目标角度
    aim_angle=sim.copy()
    for i in range(len(aim_angle)):
        for j in range(len(aim_angle)):
            aim_angle[i][j]=1-aim_angle[i][j]
            aim_angle[i][j]*=90
    aim_angle=np.array(aim_angle)
    print ("目标角度\n",aim_angle)

##将list元素归一化
def list_normalization(list):
    lsum=sum(list)
    for i in range(len(list)):
        list[i]/=lsum
    return list

##输入两个向量返回向量夹角
def get_angle(v1,v2):
    ##公式为cosθ=(x1x2+y1y2)/[√(x1²+y1²)*√(x2²+y2²)]
    numerator=sum([v1[i]*v2[i] for i in range(len(v1))])
    denominator=(sum([v1[i]**2 for i in range(len(v1))])**0.5)*(sum([v2[i]**2 for i in range(len(v2))])**0.5)
    
    cos=numerator/float(denominator)
    theta=math.acos(cos)/float(2*math.pi)*360
    return theta

##如果是三维可以绘制示意图
#def draw_pic(vector):
#    fig = plt.figure()
#    ax = fig.add_subplot(1,1,1, projection='3d')
#    
#    x=np.linspace(0,vector[0][0])
#    y=np.linspace(0,vector[0][1])
#    z=np.linspace(0,vector[0][2])
#    ax.plot(x, y, z, label='vector[0]')
#    
#    x=np.linspace(0,vector[1][0])
#    y=np.linspace(0,vector[1][1])
#    z=np.linspace(0,vector[1][2])
#    ax.plot(x, y, z, label='vector[1]')
#    
#    x=np.linspace(0,vector[2][0])
#    y=np.linspace(0,vector[2][1])
#    z=np.linspace(0,vector[2][2])
#    ax.plot(x, y, z, label='vector[2]')
#    ax.legend()
#    plt.show()
#    return ax

##代价函数∑(θ(src,i)-Aimθ(src,i))**2,i=0:src
def cost_function(src,Cangle):
    global aim_angle
    cost=sum([(Cangle[i]-aim_angle[i][src])**2
          for i in range(0,src)])
    return cost


##当前src向量基于代价最小方向移动
##直接改变的是向量而非角度
def optimal_go(src,step=0.2):
    global current_angle
    print("\n第%d个向量进行最优移动"%src)
    # step=0.2
    min_cost=float("inf")
    optimal_vector=[]
    optimal_src=0
    optimal_angle=[]
    for i in range(0,src):
        if i==src:
            continue
        Cvector=np.array(vector[src]).copy()
        ##对每个向量方向分别试探，以计算代价函数
        ##每次只从靠近一个向量的方向试探
        Cvector[i]+=step
        # print(Cvector)
        Cangle = current_angle[src].copy()  ##重新生成的角度关系
        Cangle[i]=get_angle(vector[i],Cvector)
        # print(Cangle)
        cost=cost_function(src, Cangle)
        if min_cost>cost:
            min_cost=cost
            optimal_vector=Cvector
            optimal_angle=Cangle
            optimal_src=i

    # print(optimal_src)
    Nvector=np.array(vector).copy()##新向量
    Nvector[src]=optimal_vector#list_normalization(optimal_vector)##归一化后的新向量
    Nangle=current_angle.copy()##新角度
    Nangle[optimal_src][src]=Nangle[src][optimal_src]=optimal_angle[optimal_src]
    return Nvector,Nangle,cost,optimal_src

##主函数
def execute(sim,sim_or_vector="sim"):
# if __name__=="__main__":
    # sim = np.array(
    #     [[1, 0.1, 0.8],
    #      [0.1, 1, 0.9],
    #      [0.8, 0.9, 1]])
    # sim_or_vector = "sim"
    
    if sim_or_vector=="vector":##通过逼近角度的方法生成向量坐标
        global vector
        global current_angle
        global aim_angle
        # print sim,"######"
        count_angle(sim)
        vector=np.eye(len(sim))
        start_time=time.time()
        # draw_pic()

        #get_angle([1,0,0,0],[1,1,1,0])
        current_angle=np.zeros((len(sim),len(sim)))##获取向量之间的当前角度关系
        for i in range(1,len(vector)):
            for j in range(i):
                current_angle[i][j]=get_angle(vector[i],vector[j])
                current_angle[j][i]=get_angle(vector[i],vector[j])
#        print ("当前角度关系：\n",current_angle)

        ##对每个src向量进行方向调整
        for src in range(1,len(vector)):
            steps=[]
            cost=float("inf")
            cost_list=[cost]##监控最近两个cost，使得cost接近0时停止
            while(len(cost_list)>=1):
                Nvector,Nangle,cost,step=optimal_go(src,step=min(0.05,0.01+cost/100))
                if cost_list[-1]<cost:
                    print("COST=%f,舍弃"%cost)
                    break
                else:
                    # print "------->",cost_list[-1]-cost
                    steps.append(step)
                    vector=Nvector
#                    global current_angle
                    current_angle=Nangle
#                    print ("当前向量\n",vector)
#                    print ("当前角度\n",current_angle)
                    cost_list.append(cost)
                    print ("COST=",cost)
                    # draw_pic(vector)
            print("第%d个向量调整完成，路径为：%s"%(src,steps))
        print("\n所有向量调整完成")
        for i in range(len(vector)):##归一化
            vector[i]=list_normalization(vector[i])
        vector=np.array(vector)
        # ax=draw_pic(vector)
#        ax=draw_pic(vector)
        # ax.scatter(0.5,0.6,0.7)
        print ("目标角度\n",aim_angle)
        print ("当前角度\n",current_angle)
        print ("最终向量\n",vector)
        print("累计时间\n%s秒"%(time.time()-start_time))
#        plt.show()
        return vector
    elif sim_or_vector=="sim":##直接使用相似度作为向量坐标表示
        # ax = draw_pic(sim)
        print ("最终向量\n",sim)
#        plt.show()
        return sim
