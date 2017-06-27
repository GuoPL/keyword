# -*- coding: utf-8 -*-
# usr/bin/env python
#
# Copyright@2016 R&D
#
# Author: PeilunGuo <guopeilun123@gmail.com>
#
# 2016/12/25
#
'''
calculate the average time and the overlap
'''

def readdata(file):
	for line in file:
		yield line.strip().split('\001')

def getdata(filename):
	file=open(filename)
	data=list(readdata(file))
	return data

def add(x,y):
	return x+y

def pickdata():
	i,j,dat,temp=0.0,0.0,[],['0.0']*4
	data=getdata(filename)
	for ele in data:
		if ele[2:6] != temp:
			dat.append(ele[2:10])
			i+=1
			if ele[6:10] != temp:
				j += 1
		elif ele[6:10] != temp:
			dat.append(ele[2:10])
			j += 1
	print i,j
	k,m=0,0
	for elem in dat:
		if float(elem[1])<-0.002:
			elem[1]=0
			k += 1
		if float(elem[5])<-0.03:
			elem[5]=0
			m += 1
	return dat,i,j,k,m
	
def getaverage():
	dat,i,j,k,m=pickdata()
	sum=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]	
	for ele in dat:
		el=[float(item) for item in ele]
		sum = map(add,sum,el)
	a3=[str(item/i) for item in sum[:4]]
	a4=[str(item/j) for item in sum[4:]]
	return a3+a4,float(k)/len(dat),float(m)/len(dat)

def main():
	l,r3,r4=getaverage()
	fo.write('\001'.join(l)+'\n')
	fo.write('the rate of not better than jieba and text is: {0} {1}'.format(r3,r4))
	fo.close()

filename='../result/findm4jz_1.txt'
fo=open('../result/average1_f.txt','w')
main()
print 'finished'
	
