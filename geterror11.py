# -*- coding: utf-8 -*-
#!/usr/bin/env python
# coding=utf-8
#
# Copyright @2016 R&D
#
# Author: PeilunGuo <guopeilun123@gmail.com>
#
# 2016/12/24
#

'''
Get the time between motif and jieba and textrank4zh
'''
import os
from textrank4zh import TextRank4Keyword
import jieba.analyse
import time
import networkx as nx
from itertools import combinations
from collections import Counter
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def readdata(file):
    for line in file:
	yield line.strip().split('\001')

def getdata(filename):
    file = open(filename)
    data = list(readdata(file))
    file.close()
    return data

def Spllist(lis,n):
    l = list(lis[i:i+n] for i in xrange(0,len(lis),n/2))
    return l

def Comlist(lis):
    l = []
    for elem in lis[:len(lis)/2]:
        for item in lis[len(lis)/2:]:
            l.append((elem,item))

    for ele in combinations(lis[:len(lis)/2],2):
        l.append(ele)
    return l

def GetTop(Dict,k):
    Dic={}
    for item in [i for i in Dict.items() if i[1]>k]:
        Dic[item[0]]=item[1]
    return Dic

def Getdict(ele,n,k): 
    dic={} 
    lis=Spllist(ele,n)
    for item in lis:
        li = Comlist(list(set(item)))
        for el in li:
            dic[el]=dic.setdefault(el,1)+1
    for e in combinations(list(set(lis[-1][n/2:])),2): #2016-10-31完善
    	dic[e]=dic.setdefault(e,1)+1
    
    di = GetTop(dic,k)
    return di

def getedge(con,n,k):
	list_edge=[]
	dic = Getdict(con.split(' '),n,k)
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
#	network_dic=createNetworkDic(eli,n,m)
	for key in network_dic.keys():
		for i in xrange(len(network_dic[key])-1):
			for j in xrange(i+1,len(network_dic[key])):
				for k in network_dic[network_dic[key][i]]:
					if k in network_dic[network_dic[key][j]] and k != key:
						mot400.append([key,network_dic[key][i],network_dic[key][j],k])	
	return mot400
		
def findMotif300(network_dic):
	mot300=[]
#	network_dic=createNetworkDic(eli,n,m)
	for key in network_dic.keys():
		for i in xrange(0,len(network_dic[key])-1):
			for j in xrange(i+1,len(network_dic[key])):
				if network_dic[key][i] in network_dic and network_dic[key][j] in network_dic[network_dic[key][i]]:
					mot300.append([key,network_dic[key][i],network_dic[key][j]])
	return mot300
				
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

def getMotifWord(mot):
	dic_m,Mword={},[]
	for ele in mot:
		for el in ele:
#			if el not in Mword:
			Mword.append(unicode(el,"utf-8"))
				#print chardet.detect(el)
	for ele in Mword:
		dic_m[ele]=dic_m.setdefault(ele,0)+1
	di=dict(filter(lambda x: x[1]>17, dic_m.items()))
#	print ' '.join(di.keys())
	return di.keys()
	
def countNum(li,lis):
	dic={}
	for ele in li:
		if len(ele) >=2:
			for elem in lis:
				if ele == elem:
					dic[ele]=dic.setdefault(ele,1)+1
	
	l=[]
	i=0
	for key in dic:
		l.append(key)
		l.append(str(dic[key]))	
		i+=dic[key]
	try:
		l.append(str(i/len(dic)))
	except:
		l.append('0')
	return l

def getstopword():
	stopl=[]
	file=open('../../stopword.txt','r')
	for line in file:
		stopl.append(line.strip())
	return stopl

def cutstr(str):
	sl=list(jieba.cut(str))
	stopl=getstopword()
	sr=list(set(sl)-set(stopl))
	return sr
	
def getratio300(ele,network_dic,tt):
	mt1=time.clock()
	Mot300=findMotif300(network_dic)
	Mword=getMotifWord(Mot300)
	mt2=time.clock()
	if len(Mword):
#		print '300'
		mt4=time.clock()
		keyword=getkeywordj(ele[0],len(Mword))
		mt3=time.clock()
		Mt=mt2-mt1+tt
		Kt=mt3-mt4
		try:
			KMt3=(Kt-Mt)/Kt
		except:
			KMt3=0.0
		MKl=list(set(keyword)&set(Mword))
		MK3=float(len(MKl))/len(keyword)

		mtz4=time.clock()
		keywordz=getkeywordz(ele[0],len(Mword))
		mtz3=time.clock()
		Ktz=mtz3-mtz4
		try:
			KMtz3=(Ktz-Mt)/Ktz
		except:
			KMtz3=0.0
		MKlz=list(set(keywordz)&set(Mword))
		MKz3=float(len(MKlz))/len(keywordz)
		return [KMt3,KMtz3]
	else:
		return [0.0,0.0]

def getratio400(ele,network_dic,tt):
	mt1=time.clock()
	Mot400=findMotif400(network_dic)
	Mword=getMotifWord(Mot400)
	mt2=time.clock()
	if len(Mword):
		mt4=time.clock()
		keyword=getkeywordj(ele[0],len(Mword))
		mt3=time.clock()
		Mt=mt2-mt1+tt
		Kt=mt3-mt4
		try:
			KMt4=(Kt-Mt)/Kt
		except:
			KMt4=0.0
		MKl=list(set(keyword)&set(Mword))
		MK4=float(len(MKl))/len(keyword)

		mtz4=time.clock()
		keywordz=getkeywordz(ele[0],len(Mword))
		mtz3=time.clock()
		Ktz=mtz3-mtz4
		try:
			KMtz4=(Ktz-Mt)/Ktz
		except:
			KMtz4=0.0
		MKlz=list(set(keywordz)&set(Mword))
		MKz4=float(len(MKlz))/len(keywordz)
		return [KMt4,KMtz4]
	else:
		return [0.0,0.0]

def getmax(li,lt,l_a,m):
	for i in xrange(len(lt)):
		if lt[i]<l_a[i]:
			lt[i]=l_a[i]
			li[i+1]=m
	return li,lt	

def add(a,b):
	return a+b

def getresult(elem):
	for m in xrange(4,M):
		tt1=time.clock()
		network_dic=createNetworkDic(elem[0],n,m)
		tt2=time.clock()
		tt=tt2-tt1
		l3=getratio300(elem,network_dic,tt)
		l4=getratio400(elem,network_dic,tt)		
	return l3+l4

def main():
	fo=open(path1+'error11.txt','w')
	fili=[elem for elem in os.listdir(path)]
	for ele in fili:
		filename=path+ele
		data=getdata(filename)
		i=0
		for elem in data:
			li=getresult(elem)
			li=[str(el) for el in li]
			fo.write('\001'.join(li)+'\n')
	fo.close()
		

path='../data/'
path1='../result/'
n=20
M=5
T=1
main()
print 'finished'

