# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding=utf-8
#
# Copyright @2017 R&D
#
# Author: PeilunGuo <guopeilun123@gmail.com>
#
# 2017/3/13 2017/3/17 2020/03/03
#

'''
test the method based on Motif for keywords extraction
'''
import codecs
from textrank4zh import TextRank4Keyword,TextRank4Sentence
from snownlp import SnowNLP
import jieba
import time
from itertools import combinations
import re


def Spllist(lis,n):
    l = list(lis[i:i+n] for i in xrange(0,len(lis),n/2))
    return l

def Comlist(lis):
    l = []
    for ele in combinations(lis,2):
        l.append(ele)
    return l

def GetTop(Dict,k):
    Dic={}
    for item in [i for i in Dict.items() if i[1]>k]:
        Dic[item[0]]=item[1]
    return Dic

def Getdict(ele,n,k): 
    dic={}
#    li = Spllist(' '.join(ele),n) 不按句子分, 自定义长度构建网络
    for item in ele:
        li = Comlist(item)
        for el in li:
            dic[el]=dic.setdefault(el,1)+1
    di = GetTop(dic,k)
    return di

def getedge(con,n,k):
    list_edge=[]
    dic = Getdict(con,n,k)
    for ele in dic.keys():
        list_edge.append(ele)
    return list_edge

def createNetworkDic(con,n,k):
    network_dic={}
    list_edge=getedge(con,n,k)
    for ele in list_edge:
        if ele[0] in network_dic:
            if ele[1] in network_dic[ele[0]]:
                continue
            else:
                network_dic[ele[0]].append(ele[1])
        else:
            network_dic.setdefault(ele[0],[ele[1]])

        if ele[1] in network_dic:
            if ele[0] in network_dic[ele[1]]:
                continue
            else:
                network_dic[ele[1]].append(ele[0])
        else:
            network_dic.setdefault(ele[1],[ele[0]])
    return network_dic

def findMotif400(network_dic):
    mot400=[]
    for key in network_dic.keys():
        for i in range(len(network_dic[key])-1):
            for j in range(i+1,len(network_dic[key])):
                for k in network_dic[network_dic[key][i]]:
                    if k in network_dic[network_dic[key][j]] and k != key:
                        mot400.append([key,network_dic[key][i],network_dic[key][j],k])    
    return mot400
        
def findMotif300(network_dic):
    mot300=[]
    for key in network_dic.keys():
        for i in range(0,len(network_dic[key])-1):
            for j in range(i+1,len(network_dic[key])):
                if network_dic[key][i] in network_dic and network_dic[key][j] in network_dic[network_dic[key][i]]:
                    mot300.append([key,network_dic[key][i],network_dic[key][j]])
                elif network_dic[key][j] in network_dic and network_dic[key][i] in network_dic[network_dic[key][j]]:
                    mot300.append([key,network_dic[key][j],network_dic[key][i]])
    return mot300
                
def getMotifWord(mot,keywords_num):
    Mword,dic_m=[],{}
    for ele in mot:
        for el in ele:
            Mword.append(el)
    for ele in Mword:
        dic_m[ele]=dic_m.setdefault(ele,0)+1
    dic=list(sorted(dic_m.items(), key=lambda x: x[1], reverse=True))
    return dic[:keywords_num]

def get_abstract(M,article,source,len_A):
    dic={}
    for i in range(len(article)):
        dic[i]=len(set(M)&set(article[i]))

    Mr= sorted(dic.items(), key=lambda x:x[1], reverse=True)

    temp=[source[key[0]] for key in Mr][:len_A]
    return temp
    
def getStop():
    fil=codecs.open('./stopword.txt','r','utf-8')
    stop=[]
    for line in fil:
        stop.append(line.strip())
    return stop

def getkeywordz(eli,topK):
    tags=[]
    tr4w=TextRank4Keyword()
    tr4w.analyze(text=eli, lower=True, window=2)
    keyword=tr4w.get_keywords(topK,word_min_len=1)
    for item in keyword:
        tags.append(item.word)
    return tags

def getkeywordj(eli,topK):
    tags=jieba.analyse.extract_tags(eli,topK)
    return tags

def main():
    p = r'[。！？;]' #划分句子的分割符
    text = """希腊报告首起非洲猪瘟疫情    　　新华
      社雅典2月6日电(记者于帅帅 李晓鹏)希腊农业发展和食品部6日宣布，该国东北部塞雷斯地区一家小型养猪场发生非洲猪瘟。这是希腊报告的首起非洲猪瘟疫情，政府表示将采取一系列紧急措施控制疫情扩散。 　　在当天>      于首都雅典举行的新闻发布会上，希腊农业发展和食品部长马基斯·沃里季斯说，疫情发现地区的猪肉出口交易已暂停，该养猪场及周围3公里以内所有养殖猪已被宰杀，以养猪场为中心方圆10公里以内，未来40天禁止任何活
      体动物或其废弃物转移。工作人员将开展检测工作以追踪病毒来源。 　　“我们对此非常警惕，也绝对有能力恰当处理并控制疫情扩散”，沃里季斯说。他同时强调，非洲猪瘟病毒不会感染人类。 　　目前波兰、罗马尼亚、
      匈牙利等欧洲国家已发生非洲猪瘟疫情。非洲猪瘟是由非洲猪瘟病毒感染猪引起的一种急性、出血性、烈性传染病，以高热、内脏器官严重出血和高死亡率为特征。非洲猪瘟不是人畜共患病。"""
    article = re.split(p, text)
    print(article)
    stop=getStop()
    data=[list(set(jieba.cut(ele))-set(stop)) for ele in article]
#        ti=time.clock()
    network_dic=createNetworkDic(data,n,m)
    M3=getMotifWord(findMotif300(network_dic),keywords_num = 10) #M3性能好，效果也不错
#    # keywords_num：提取的关键词数量
    print(M3) #输出基于M3提取的关键词
#    M4=getMotifWord(findMotif400(network_dic),keywords_num = 10)  #M4相对M3性能较差，但是效果相对较好。
#    print(M4) #输出基于M4提取的关键词
    kz = getkeywordz(article,10)
    print(kz)
    kj = getkeywordj(article,10)
    print(kj)


m=4 #构建的网络的边的阈值
n=20 #基于长度构建网络的边界,暂定为基于句子提取。如果用户需要，可以调整42行代码，基于边界提取。
main()
#fo.close()
print ('finished')