# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 12:24:02 2018
《新闻的可信度评判与分析系统》
微信交互：程序入口
@author: aidc0082
"""

import requests
import itchat
import MainLine

KEY = '8edce3ce905a4c1dbb965e6b35c3834d'


state=0
news=object
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    global state
    global news
    nickname=itchat.search_friends(userName=msg['FromUserName'])['NickName']
    defaultReply = nickname+': ' + msg['Text']
    
    print(defaultReply)
    if True:
        if msg['Text'] == u"中兴事件" or msg['Text'] == u"1":
            news, n_clusters_ = MainLine.execute(msg['Text'], msg.user,demo=1)
        else:
            news, n_clusters_ = MainLine.execute(msg['Text'],msg.user)
        msg.user.send("找到的新闻有：")
        for i in range(len(news)):
            reply = u"《%s》\n#来自%s %s发布#\n摘要： "%(news[i].Title,news[i].PressName,news[i].Time)
            for j in range(len(news[i].Sentences)-1):
                reply+=news[i].Sentences[j]
            if len(news[i].Sentences)==1:
                reply += news[i].Sentences[0]
            reply+="\n查看全文：%s\n文章情感：%s\n观点归类：第%s类观点\n可信度：%s(%s)" % (news[i].URL,str(news[i].Sentiment)[:5],news[i].Cluster+1, str(news[i].Reliability)[:5], "★" * int(news[i].Reliability * 5+1))
            msg.user.send(reply)

        msg.user.send(u"加载完成，以上是新闻的摘要。")
        import NewsAnalyzing
        analysis=NewsAnalyzing.execute(msg['Text'],news,n_clusters_)
        msg.user.send(analysis)

#        msg.user.send(reply)
    return None



itchat.auto_login(hotReload=True)
itchat.run()