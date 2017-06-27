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
	xy=[[],[],[],[],[],[],[],[],[],[],[],]
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
        c=['b','r','m','g','c','y','k']

        for i in xrange(len(m)):
                plt.sca(m[i])
                plt.plot(xy[0],xy[i+1],c[i])
                plt.title(T[i])
                plt.xlabel('topK')
                plt.ylabel('overlap')
        fig.show()
        fig.savefig('../picture/mjz_jac_f.png')

        fig_n=plt.figure(3)
        m3=plt.subplot(321)
        j3=plt.subplot(322)
        z3=plt.subplot(323)
        m4=plt.subplot(324)
        j4=plt.subplot(325)
        z4=plt.subplot(326)
        m_n=[m3,j3,z3,m4,j4,z4]
        T_n=['m3','j3','z3','m4','j4','z4']

        for j in xrange(len(m_n)):
            plt.sca(m_n[j])
            plt.plot(xy[0],xy[j+5])
            plt.title(T_n[j])
            plt.xlabel('topK')
            plt.ylabel('keyword_average')
        fig_n.show()
        fig_n.savefig('../picture/mjz_n_f.png')

def main():
        data=getdata(filename)
        xy=getxy(data)
        plotxy(xy)
	
filename='../result/jaccard1.txt'
main()
print 'finished'
