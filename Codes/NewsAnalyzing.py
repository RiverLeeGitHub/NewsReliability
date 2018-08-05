# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import requests
import json
import re
from bosonnlp import BosonNLP

def emotion(news,cluster):
    # nlp = BosonNLP('3KJW0U-I.24870.1PdhvJB30HgY')
    # combine = ""
    # for i in range(len(news)):
    #     print("cluster",cluster)
    #     if news.Cluster==cluster:
    #         for s in news[i].Sentences:
    #             combine+=s
    #     print("combine:",combine)
    #     sentiment = nlp.sentiment(combine)
    #     print("sentiment",sentiment)
    sentiment=0
    count=0
    for i in range(len(news)):
        if news[i].Cluster==cluster:
            sentiment+=news[i].Sentiment
            count+=1
    sentiment/=count
    exception=[]
    dist=float("inf")
    delegate=object
    for i in range(len(news)):
        if news[i].Cluster==cluster:
            if abs(sentiment-news[i].Sentiment)>0.5:
                exception.append(news[i])
            if abs(sentiment-news[i].Sentiment)<dist:
                delegate=news[i]
    return sentiment,exception,delegate

def closest_new(news,cluster):
    dist=float("inf")
    delegate=object
    for i in range(len(news)):
        if news[i].Cluster==cluster:
            if news[i].DistToCentroid<dist:
                delegate=news[i]
    return delegate


def summary(new):
    rawtext=new.RawText
    SUMMARY_URL = 'http://api.bosonnlp.com/summary/analysis'
    # 注意：在测试时请更换为您的API Token
    headers = {'X-Token': 'iVr388Im.25213.akIYrDR90nCB'}
    def trim(List):
        text=[]
        for i in range(len(List)):
            if len(List[i])>0:
                text.append(List[i])
        return text
    source = {
            'not_exceed': 0,
            'percentage': 10,#10,#0.2, # 原文的20%也不是很短，可以改成50（50字）
            'title': '',
            'content': rawtext
        }
    resp = requests.post(
        SUMMARY_URL,
        headers=headers,
        data=json.dumps(source).encode('utf-8'))
    resp.raise_for_status()
#    print(resp.text)
    text=re.split(r'[\\n|\\t]',resp.text[1:-1])
#    print("!",text)
    text=trim(text)
#    print("!@@",text)
    return text

def execute(keyword,news,n_cluster):
    analysis = u"我们对上述新闻做了简要的分析：\n    "
    if n_cluster==1:

        analysis+=u"在我们找到的关于%s新闻中，媒体的观点较为统一。" %(keyword)
        aver_senti,exception,delegate=emotion(news,cluster=0)
        if aver_senti>=0.6:
            if len(exception)>0:
                analysis += u"除了"
                for i in range(len(exception)-1):
                    analysis += exception[i].PressName+"、"
                analysis+=exception[-1].PressName
                analysis+="这%s家媒体外，"%(len(exception))
            analysis += u"大家对%s的态度大多很积极，代表媒体是%s。" % (keyword,delegate.PressName)


        elif aver_senti <= 0.4:
            if len(exception) > 0:
                analysis += u"除了"
                for i in range(len(exception)-1):
                    analysis += exception[i].PressName+"、"
                analysis+=exception[-1].PressName
                analysis += "这%s家媒体外，" % (len(exception))
            analysis += u"大家对%s的态度大多不太乐观，代表媒体是%s。" % (keyword,delegate.PressName)

        else:
            if len(exception) > 0:
                analysis += u"除了"
                for i in range(len(exception)-1):
                    analysis += exception[i].PressName+"、"
                analysis+=exception[-1].PressName
                analysis += "这%s家媒体外，" % (len(exception))
            analysis += u"大家对%s的态度总体平平，代表媒体是%s。" % (keyword,delegate.PressName)

    elif n_cluster==2:
        analysis += u"关于%s，大家的观点可以大致分为两类。一类是以%s为代表的新闻，"%(keyword,closest_new(news,0).PressName)
        print(closest_new(news,0).Sentiment)
        if closest_new(news,0).Sentiment>0.7:
            analysis += u"持有比较积极的态度，"
        elif closest_new(news,0).Sentiment<0.3:
            analysis += u"态度不太乐观，"
        else:
            analysis += u"态度较为中立，"

        analysis += "另一类的代表是%s，"%(closest_new(news,1).PressName)
        if closest_new(news,1).Sentiment>0.7:
            analysis += u"态度较好"
        elif closest_new(news,1).Sentiment<0.3:
            analysis += u"态度有点消极"
        else:
            analysis += u"态度中立"
        analysis += "。看完以上的新闻，相信您会对%s有更加全面和清晰的认识。"%(keyword)

    else:
        analysis += u"关于%s的观点可谓百家争鸣。按列举的新闻来看，有大致%s类观点。可能媒体从多种方面对此进行了阐述，也有可能对同一事件有不同的态度，有辩证思考的空间。" % (keyword,n_cluster)
    # for i in range(len(news)):
    #     analysis+="\n%s"%summary(news[i])
    return analysis