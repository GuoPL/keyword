# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright@2016 R&D
# 
# Author: Peilun Guo <guopeilun123@gmail.com>
#
# 2016/12/05
#

'''
Get the best m of one article
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def readdata(file):
	for line in file:
		yield line.strip().split('\001')

def getdata(filename):
	file=open(filename)
	data=list(readdata(file))
	return data

def compare(li,ele,lr):
	for i in xrange(len(li)):
		if li[i] <= float(ele[i+2]):
			lr[i]=ele
			li[i]=float(ele[i+2])
	return li,lr
		
def getmax(data):
	li,lr=[0.0]*8,[str(0)]*8
	i=0
	for ele in data:
		li,lr=compare(li,ele,lr)
		i+=1
		print i
	return lr

def main():
	data=getdata(filename)
	lr=getmax(data)
	for ele in lr:
		fo.write('\001'.join(ele)+'\n')
	fo.close()

fo=open('../result/max.txt','w')
filename='../result/m4jzh.txt'
main()
print 'finished'
