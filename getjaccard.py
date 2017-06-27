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
Get the jacaard similarity of motif, 4zh and jieba with whose overlap
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

def getjaccard(lis,li):
	d=list(set(lis)&set(li))
	try:
		return len(d)/float(len(set(lis) | set(li)))
	except:
		return 0.0

def gettopK(dic,topK):
	lr,sum=[],0.0
	lk=dict(filter(lambda x: x[1] >topK, dic.items()))
	for key in lk:
		lr.append({'name':key,'value':dic[key]})
		sum += float(dic[key])
	return lr,lk.keys(),sum

def writeFile(list,separate):
	fo=open(path1+'m4'+separate+'.json','w')
	json.dump(list,fo)
	fo.close()

def getlist():
	all=[[],[],[],[],[],[]]
	i = 0
	data=getdata(filename)
	for elem in data:
		if (elem[10].split('m3')):
			all[0]+=elem[10].split('m3')
			all[1]+=elem[11].split('j3')
			all[2]+=elem[12].split('z3')
			all[3]+=elem[13].split('m4')
			all[4]+=elem[14].split('j4')
			all[5]+=elem[15].split('z4')
			i += 1
	return all,i

def getkey(topK):
	la,sum=[],[]
	all,l=getlist()
	separate=['m3','j3','z3','m4','j4','z4']
	for i in xrange(len(separate)):
		dic=getdict(all[i])
		lr,lk,su=gettopK(dic,topK)
		writeFile(lr,separate[i])		
		la.append(lk)
		sum.append(su)
	return la,l,sum
	
def getpro(topK):
	la,len,sum=getkey(topK)
	mj3=getjaccard(la[1],la[0])
	mz3=getjaccard(la[2],la[0])
	mj4=getjaccard(la[4],la[3])
	mz4=getjaccard(la[5],la[3])
	average=[ele/len for ele in sum]
	return [mj3,mz3,mj4,mz4]+average
	
def main():
	for topK in xrange(5,201):
		l=getpro(topK)
		li=[str(ele) for ele in l]		
		fo.write(str(topK)+'\001'+'\001'.join(li)+'\n')

path1='../result/jaccard/'
fo=open('../result/jaccard1.txt','w')
filename='../result/findm4jz_1.txt'
main()
print 'finished'


		 


