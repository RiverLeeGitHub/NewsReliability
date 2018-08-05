# -*- coding: UTF-8 -*-
#import urllib, urllib2, sys
import ssl
import json
import requests
import numpy as np
import sys
#reload(sys)
#sys.setdefaultencoding('gbk')

from aip import AipNlp
APP_ID = '10993617'
API_KEY = 'MFlYuFe6Ci5nITE0emRWnqwL'
SECRET_KEY = 'cHg1Q7hwTLmitkujQRKiHMYHr3gSrf97'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

def similarity(statements):
    combination=[]
    sim=np.ones((len(statements), len(statements)))
    for i in range(1,len(statements)):
        for j in range(i):
            combination.append((statements[i],statements[j],i,j))
    process=0
    for pair in combination:
#        print((pair[0][:3],pair[1][:3]))
        # client.simnet(pair[0], pair[1])
        options = {}
        options["model"] = "CNN"
        # print(pair[0])
        # pair[0]=pair[0].replace(u'\xa9', u'')
        # pair[1]=pair[1].replace(u'\xa9', u'')
        # print(pair[0].__class__)
        # print(pair[1].__class__)
        try:
            score = client.simnet(pair[0], pair[1], options)[u'score']
    #        print(score)
            sim[pair[2], pair[3]], sim[pair[3], pair[2]] = score, score
            process+=100/len(combination)
            sys.stdout.write(str(process)+"%\n")#r")  # 这两句打印字符到终端
            sys.stdout.flush()
        except:
            continue
    return sim

def execute(statement):
#    statements=statement
    
    sim=similarity(statement)
#    print(sim)
    return sim

# def validate():
#     # client_id 为官网获取的AK， client_secret 为官网获取的SK
#     host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MFlYuFe6Ci5nITE0emRWnqwL&client_secret=cHg1Q7hwTLmitkujQRKiHMYHr3gSrf97'
#     headers = {"Content-Type": "application/json"}
#
#     request = urllib2.Request(host)#,data=json.dumps(body),headers=headers)
#     #request = urllib2.urlopen(host,data=json.dumps(body))
#     request.add_header('Content-Type', 'application/json; charset=UTF-8')
#     response = urllib2.urlopen(request)
#     content = response.read()
#
#     res = requests.get(host)
#     json_data = json.loads(res.text)
#
#     # if (content):
#         # print(content)
#         # print(json_data['access_token'])
#
#     access_token=json_data['access_token']
#
#     host='https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?access_token='+access_token
#     return host,headers
#
# def similarity(sim):
#     combination=[]
#     for i in range(1,len(statements)):
#         for j in range(i):
#             combination.append((statements[i],statements[j],i,j))
#     process=0
#     for pair in combination:
#         # print [p[:15] for p in pair[:2]]
#         host,headers=validate()
#         body={"text_1": pair[0],"text_2": pair[1]}
#
#         request = urllib2.Request(host,data=json.dumps(body),headers=headers)
#         #request = urllib2.urlopen(host,data=json.dumps(body))
#         request.add_header('Content-Type', 'application/json; charset=UTF-8')
#         response = urllib2.urlopen(request)
#         content = response.read()
#         score = float(content[content.find("\"score\":")+8:-1])
#         # print score
#
#         sim[pair[2],pair[3]],sim[pair[3],pair[2]]=score,score
#         process+=100/len(combination)
#         sys.stdout.write(str(process)+"%\r")  # 这两句打印字符到终端
#         sys.stdout.flush()
#     sys.stdout.write("100%\r")  # 这两句打印字符到终端
#     sys.stdout.flush()
#     # print sim
#     return np.array(sim)
#
# def execute(statement):
#     statements=statement
#     sim=np.ones((len(statements), len(statements)))
#     return similarity(sim)