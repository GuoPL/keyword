# -*- coding: utf-8 -*- 
#!/usr/bin/env python
#
# Copyright@2016 @R&D
#
# Author: Peilun Guo <guopeilun123@gmail.com>
#
# 2016/12/21
#
'''
Plot the overlap of motif and jieba and textrank about topK
'''

import matplotlib.pyplot as plt
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

def getxy(data):
	xy=[[],[],[],[],[]]
	for ele in data:
		for i in xrange(len(ele)):
			xy[i].append(float(ele[i]))
	return xy

def plotxy(xy):
	fig=plt.figure(2)
	mj3=plt.subplot(221)
        mz3=plt.subplot(222)
        mj4=plt.subplot(223)
        mz4=plt.subplot(224)
        m=[mj3,mz3,mj4,mz4]
        T=['mj3','mz3','mj4','mz4']
        c=['b','r','m','g']

        for i in xrange(len(m)):
                plt.sca(m[i])
                plt.plot(xy[0],xy[i+1],c[i])
                plt.title(T[i])
                plt.xlabel('topK')
                plt.ylabel('overlap')

        fig.show()
        fig.savefig('../picture/mjz1.png')
            
def main():
        data=getdata(filename)
        xy=getxy(data)
        plotxy(xy)
	
filename='../result/overlap1.txt'
main()
print 'finished'
