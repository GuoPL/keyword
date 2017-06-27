# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright@2017 R&D
#
# Author: Peilun Guo <guopeilun123@gmail.com>
#
# 2017/1/2
#
'''
Get the keyword's length of motif, 4zh and jieba 
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

def getkey():
	la=[]
	all=getlist()
	separate=['m3','j3','z3','m4','j4','z4']
	for i in xrange(len(separate)):
		dic=getdict(all[i])
		la.append(len(dic))
	return la
	
def main():
	la=getkey()
	lr=[str(item) for item in la]
	fo.write("the length of m3's keywords is {0}".format(lr[0])+'\n')
	fo.write("the length of j3's keywords is {0}".format(lr[1])+'\n')
	fo.write("the length of z3's keywords is {0}".format(lr[2])+'\n')
	fo.write("the length of m4's keywords is {0}".format(lr[3])+'\n')
	fo.write("the length of j4's keywords is {0}".format(lr[4])+'\n')
	fo.write("the length of z4's keywords is {0}".format(lr[5])+'\n')
	fo.close()

fo=open('../result/keywordlen1.txt','w')
filename='../result/findm4jz_1.txt'
main()
print 'finished'


		 


