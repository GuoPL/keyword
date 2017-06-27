# -*- coding: utf-8
#!/usr/bin/env python
#
# Copyright@2016 @R&D
#
# Author: Peilun Guo <guopeilun123@gmail.com>
#
# 2016/12/6
#

'''
remove the last column
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def readdata(file):
	for line in file:
		yield line.strip().split('\001')[:-1]

def getdata(filename):
	file=open(filename)
	data=list(readdata(file))
	return data

def writedata():
	data=getdata(filename)
	for ele in data:
		fo.write('\001'.join(ele)+'\n')
	fo.close()

filename='../data/baidu04_title_share.txt'
fo=open('../data/baidu04_title_share_filter.txt','w')
writedata()
print 'finished'
