# -*- coding: utf-8 -*-
#
# Copyright@2016 R&D
#
# Author: PeiunGuo <guopeilun123@gmail.com>
#
# 2016/12/25
#
'''
get the average of error time
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

def minus(x,y):
	return x-y

def add(x,y):
	return x+y

def getnum(filenam):
	data=getdata(filenam)
	dat=[]
	for ele in data:
		el=[float(item) for item in ele]
		dat.append(el)
	return dat

def main():
	sum,temp,l=[0.0]*4,[0.0]*4,0.0
	dat1=getnum(filename1)
	dat2=getnum(filename2)
	for i in xrange(len(dat1)):
		if dat1[i] != temp and dat2[i] != temp:
			sum = map(add,map(minus,dat1[i],dat2[i]),sum)
			l += 1
	average=[str(item/l) for item in sum]
	fo.write('1'+'\n')
	fo.write('\001'.join(average)+'\n')
	print average
		
filename1='../result/error1.txt'
filename2='../result/error11.txt'
fo=open('../result/error_ave1.txt','w')
main()
print 'finished'
	
