# -*- coding: utf-8 -*-
#
# Copyright@2016 R&D
#
# Author: PeilunGuo <guopeilun123@gmail.com>
#
# 2016/12/19
#
'''
Get the best m of every column and the best m of all
'''

def readdata(file):
	for line in file:
		yield line.strip().split('\001')

def getdata(filename):
	data=list(readdata(filename))
	return data

def getdict():
	list_a,dict=[],{}
	data=getdata(filename)
	for column in xrange(1,9):
		list_m=[str(column)]
		for ele in data:
			dict[ele[column]]=dict.setdefault(ele[column],0)+1	
#		print dict
		dic_t=sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
		print dic_t
		for i in xrange(5):
			list_m.append(dic_t[i][0])
		print list_m
		list_a.append(list_m)
	return list_a

def writefile():
	lis=getdict()
	for ele in lis:
		fo.write('\001'.join(ele)+'\n')
	fo.close()

filename=open('../result/bestm1.txt','r')
fo=open('../result/best_sta1.txt','w')
writefile()
print 'finished'
