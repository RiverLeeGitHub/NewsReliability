# -*- coding: utf-8 -*-
import numpy as np
import BaiduNews
import Demostration
import math

def dist(point1,point2):
#    (x1,y1,z1)=point1
#    (x2,y2,z2)=point2
#    return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**0.5
    return math.sqrt(np.power(point1 - point2, 2).sum())

def execute(keyword,user,demo=0):
#if __name__=="__main__":
    print("\n##正在运行 网页新闻爬取")
    
    
    if demo==1:
        user.send("-> 正在寻找关于中兴事件的新闻")
        news=Demostration.execute()
        # sim=np.fromfile("ZTC.bin",dtype=np.float)
#        print(sim.shape)
#         sim.shape=17,17
    else:
        user.send("-> 正在寻找关于%s的新闻"%keyword)
        news=BaiduNews.execute(keyword)
        

    statements=[]
    for new in news:
        statements+=new.Sentences


    import SentenceSimilarity
    import VectorGeneration
    import NewsLocation

    print("\n##正在运行 语义相似度计算")
    user.send("-> 计算语义相似度")
    if demo==0:
        SentenceSimilarity.statements=statements
    sim=SentenceSimilarity.execute(statements)
    sim.tofile("ZTC.bin")
    # sim=np.array(
    #     [[1,0.3,0.4,0.2],
    #      [0.3,1,0.5,0.3],
    #      [0.4,0.5,1,0.5],
    #      [0.2,0.3,0.5,1]])
    # sim=np.array(
    #     [[1,0.1,0.8],
    #      [0.1,1,0.9],
    #      [0.8,0.9,1]])
    print("\n##正在运行 语义向量生成\n")
    user.send("-> 生成语义向量")
    vectors=VectorGeneration.execute(sim,sim_or_vector="sim")#"vector")
    print("\n##正在运行 新闻坐标点定位\n")
    user.send("-> 新闻坐标定位")
    dist_mat=NewsLocation.execute(news,vectors,statements)

    print("\n##正在运行 新闻可信度分析\n")
    user.send("-> 新闻可信度分析")
#    ##计算距离和
#    sum_SumOfDistance=0
#    for i in range(len(news)):
#        news[i].SumOfDistance=sum(dist_mat[i])
#        sum_SumOfDistance+=news[i].SumOfDistance
#
#
#    ##距离和从小到大排序
#    for i in range(len(news)):
#        for j in range(i,len(news)):
#            if news[i].SumOfDistance>news[j].SumOfDistance:
#                temp=news[i]
#                news[i]=news[j]
#                news[j]=temp
#
#    ##可信度计算
#    for i in range(len(news)):
#        news[i].Reliability = 1-news[i].SumOfDistance/sum_SumOfDistance
    from sklearn.cluster import MeanShift, estimate_bandwidth
    from sklearn.datasets.samples_generator import make_blobs
    
    X, _ = make_blobs(n_samples=1000, centers=[news[i].Coordinate for i in range(len(news))],
                                               cluster_std=0.4)##调整簇内距离，越大簇越少#0.6
    
    bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)#0.2
    
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    centroids = ms.cluster_centers_
    
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("n_clusters_",n_clusters_)
    print("centroids",centroids)
#    print("labels_unique",labels_unique)
#    print("labels",labels)
    
    sum_DistToCentroid=0
    for i in range(len(news)):
        min_dist=float("inf")
        for j in range(len(centroids)):
            if dist(news[i].Coordinate,centroids[j])<min_dist:
                news[i].Cluster=j
                min_dist=dist(news[i].Coordinate,centroids[j])
        news[i].DistToCentroid=min_dist
        sum_DistToCentroid+=min_dist
        print(news[i].Title,(news[i].Cluster),news[i].DistToCentroid)
    #可信度计算
    for i in range(len(news)):
        news[i].Reliability = 1-news[i].DistToCentroid/sum_DistToCentroid
    return news,n_clusters_#dist_mat


