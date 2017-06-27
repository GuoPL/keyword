# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright@2016 R&D
#
# Author: Peilun Guo <guopeilun123@gmail.com>
#
# 2016/12/21
#
'''
Get the keywords of motif, 4zh and jieba with whose overlap
'''

import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def readdata(file):
	for line in file:
		yield line.strip().split('\001')

def getdata(filename):
	file=open(filename)
	data=list(readdata(file))
	return data

def getdict(list):
	dict_word={}
	for ele in list:
		dict_word[ele]=dict_word.setdefault(ele,0)+1
	return dict_word

def getoverlap(lis,li):
	d=list(set(lis)&set(li))
	try:
		return len(d)/float(len(lis))
	except:
		return 0.0

def gettopK(dic,topK):
	lr=[]
	lt=sorted(dic.items(), lambda x,y: cmp(x[1],y[1]), reverse=True)
	lk=[ele[0] for ele in lt]
	for key in lk[:topK]:
		lr.append({'name':key,'value':dic[key]})
	return lr,lk[:topK]

def writeFile(list,separate):
	fo=open(path1+'m4'+separate+'.json','w')
	json.dump(list,fo)
	fo.close()

def getlist():
	all=[[],[],[],[],[],[]]
	data=getdata(filename)
	for elem in data:
		all[0]+=elem[10].split('m3')
		all[1]+=elem[11].split('j3')
		all[2]+=elem[12].split('z3')
		all[3]+=elem[13].split('m4')
		all[4]+=elem[14].split('j4')
		all[5]+=elem[15].split('z4')
	return all

def getkey(topK):
	la=[]
	all=getlist()
	separate=['m3','j3','z3','m4','j4','z4']
	for i in xrange(len(separate)):
		dic=getdict(all[i])
		lr,lk=gettopK(dic,topK)
#		writeFile(lr,separate[i])		
		la.append(lk)
	return la
	
def getpro(topK):
	la=getkey(topK)
	mj3=getoverlap(la[1],la[0])
	mz3=getoverlap(la[2],la[0])
	mj4=getoverlap(la[4],la[3])
	mz4=getoverlap(la[5],la[3])
	return [mj3,mz3,mj4,mz4]	
	
def main():
	for topK in xrange(10,30001,10):
		l=getpro(topK)
		li=[str(ele) for ele in l]		
		fo.write(str(topK)+'\001'+'\001'.join(li)+'\n')

path1='../result/json/'
fo=open('../result/overlap1.txt','w')
filename='../result/findm4jz_1.txt'
main()
print 'finished'


		 


