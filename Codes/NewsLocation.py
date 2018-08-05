# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from bosonnlp import BosonNLP
import numpy as np
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
def news_distance(coordinate1,coordinate2):
    dist=0
    for i in range(len(coordinate1)):
        dist+=(coordinate1[i]-coordinate2[i])**2
    dist=dist**0.5
    return dist

def generate_distance_matrix(news):
    mat=np.zeros((len(news),len(news)))
    for i in range(1,len(news)):
        for j in range(len(news)-1):
            mat[i][j]=news_distance(news[i].Coordinate,news[j].Coordinate)
            mat[j][i]=mat[i][j]
    return mat

def nomalization(Coordinate):
    for i in range(len(Coordinate)):
        Coordinate[i]/=sum(Coordinate)

def execute(news,vectors,statements):

    nlp = BosonNLP('3KJW0U-I.24870.1PdhvJB30HgY')
    # print("\n情感分析")
    for i in range(len(news)):
        combine=""
        for s in news[i].Sentences:
            combine+=s
#        print (news[i].PressName,"\n",combine,"\n",nlp.sentiment(combine)[0][0])
#    print("")
    for new in news:
        new.Coordinate=np.zeros(len(statements))
        for i in range(len(statements)):
            if statements[i] in new.Sentences:
                for j in range(len(vectors)):
                    new.Coordinate[j]+=vectors[i][j]
        ##坐标归一化
        nomalization(new.Coordinate)
        ##添加情感分析维度在新闻坐标里
        combine=""
        for s in new.Sentences:
            combine+=s
        sentiment=nlp.sentiment(combine)
        new.Sentiment=sentiment[0][0]
        # print (new.PressName,"\n",combine,"\n",sentiment[0][0])
        # new.Coordinate.append(sentiment[0][0])
        new.Coordinate=np.append(new.Coordinate, sentiment[0][0]*len(vectors)/2)

        print("%s %s"%(new.PressName,new.Coordinate))
    distance_matrix=generate_distance_matrix(news)
    print("\n新闻距离矩阵\n",distance_matrix)
    return distance_matrix