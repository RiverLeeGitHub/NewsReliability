# -*- coding: <utf-8> -*-
from __future__ import print_function, unicode_literals
import requests
from bs4 import BeautifulSoup
import bs4
import json
import re
import os


class New:
    PressName="PressName"
    Title=""
    RawText="RawText"
    Sentences=[]
    Coordinate=[]
    # SumOfDistance=0
    Reliability=0
    URL="URL"
    Time=""
    Cluster=-1
    DistToCentroid=-1
    Sentiment=-1
    def __init__(self,PressName,Title,Time,URL,RawText,Sentences=[]):
        self.PressName=PressName
        self.Time=Time
        self.Title=Title
        self.URL=URL
        self.RawText=RawText
        self.Sentences=Sentences
        


def MemorizeArticle(url):
    text=""
    hd = {'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers = hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
    #    title = re.search(r'[A-Za-z]+.com', url).group(0)
        for t in soup.find_all('p'):
            if isinstance(t, bs4.element.Tag) and re.match(r'link', t.text) == None and t.find(True) == None:
                if re.match(r'[\u4e00-\u9fa5|，。；？]', t.text) != "" and len(t.text) > 30:
                    if t.text.find(r'[a-zA-Z]{4,}')>=0:
                        print("continue")
                        continue
                    text+=t.text
                    # print("->",t.text)
    
        return text
    except:
        print("except")
        return None


SUMMARY_URL = 'http://api.bosonnlp.com/summary/analysis'
# 注意：在测试时请更换为您的API Token
headers = {'X-Token': 'iVr388Im.25213.akIYrDR90nCB'}
def summary(rawtext):
    def trim(List):
        text=[]
        for i in range(len(List)):
            if len(List[i])>0:
                text.append(List[i])
        return text
    source = {
            'not_exceed': 0,
            'percentage': 0.2,#80,#0.2, # 原文的20%也不是很短，可以改成50（50字）
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

def execute(word):
#    word=input('Search: ')
    news=[]
    url="http://news.baidu.com/ns?word="+word+"&tn=newstitle&from=news&cl=2&rn=20&ct=0"
    
    r=requests.get(url)
    html=r.text
    
    soup=BeautifulSoup(html,"html.parser")
    # print(soup.prettify())
    
    div_item=soup.find_all('div',class_='result title')
    # print(div_item)
    
    for div in div_item:
        a_title = div.find('h3', class_='c-title').find('a').get_text()
        a_href = div.find('h3', class_='c-title').find('a').get('href')
        a_text=div.find('div',class_='c-title-author').get_text().split('\xa0\xa0')
        a_author=a_text[0]
        a_time=a_text[1]
        print("\n《%s》"%a_title)#,end=' ')
    #    print(a_href,end=' ')
    #    print(a_author)#,end=' ')
    #    print(a_time)
        raw_text=MemorizeArticle(a_href)
    #    print(raw_text)
    #     print("@@@",raw_text)
        if raw_text!=None and len(raw_text)>10:#raw_text!=None:# and len(raw_text)>100:
            print("Added")
            sentences=summary(raw_text)
            trim_sentences=[]
            for i in range(len(sentences)):
                if len(re.findall('[a-zA-Z0-9]',sentences[i]))/len(sentences[i]) < 0.4 and len(sentences[i])>5:
                    # print("add",sentences[i])
                    trim_sentences.append(sentences[i])
            sentences=trim_sentences
            # print("####",sentences)
            if len(sentences)>0:
                news.append(New(PressName=a_author,
                                Title=a_title,
                                Time=a_time,
                                URL=a_href,
                                RawText=raw_text,
                                Sentences=sentences))
        if len(news)>=5:
            break
    for i in range(len(news)):
        news[i].Sentences.append(news[i].Title)
    return news
    