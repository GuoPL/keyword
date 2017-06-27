# -*- coding: utf-8 -*-
#
# Copyright@2016 R&D
#
# Author: PeilunGuo <guopeilun123@gmail.com>
#
# 2016/12/24
#

'''
calculate the F score 
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

def getF(x,y):
	try:
		return (2*x*y)/(x+y)
	except:
		return 0.0
	
def getallF():
	temp,Fj3,Fz3,Fj4,Fz4,i,j,k,l=['0.0']*4,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
	data=getdata(filename)
	for elem in data:
		ele=elem[2:10]
		if ele[:4] != temp:
			j3=getF(float(ele[0]),float(ele[0]))
			Fj3 += j3
			i += 1
			
			z3=getF(float(ele[2]),float(ele[2]))
			Fz3 += z3
			
		if ele[4:] != temp:
			j4=getF(float(ele[4]),float(ele[4]))
			Fj4 += j4
			j += 1

			z4=getF(float(ele[6]),float(ele[6]))
			Fz4 += z4
	return [Fj3/i,Fz3/i,Fj4/j,Fz4/j]
		
def main():
	F_all=getallF()
	F_a=[str(item) for item in F_all]
	fo.write('\001'.join(F_a))
	print F_all
	fo.close()

filename='../result/findm4jz_1.txt'
fo=open('../result/FS1.txt','w')
main()
print 'finished'
	
