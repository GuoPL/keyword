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
get the overlap between the motif and the others
'''

import sys
import os
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def getfile(file):
	for line in file:
		return json.loads(line)

def getfili(path):
	fl=[]
	for ele in os.listdir(path):
		if 'json' in ele:
			fl.append(ele)
	return fl

def getkey(lis):
	lt=[]
	for ele in lis:
		lt.append(ele['name'])
	return lt

def getoverlap(lis,li):
	print ' '.join(lis)
	print '==='
	print ' '.join(li)
	print '---'
	temp=list(set(lis)&set(li))
	print len(temp),' '.join(temp)
	try:
		return round(float(len(temp))/float(len(lis)),4)
	except:
		return 0.0

def getall():
	la=[]
	fili=getfili(path)
	print fili
	for fil in fili:
		filename=path+fil
		if 'j3' in fil:
			file=open(filename)
			lt=getfile(file)
			lj3=getkey(lt)
			print ' '.join(lj3),fil
		if 'm3' in fil:
			file=open(filename)
			lt=getfile(file)
			lm3=getkey(lt)
			print ' '.join(lm3),fil
		if 'z3' in fil:
			file=open(filename)
			lt=getfile(file)
			lz3=getkey(lt)
			print ' '.join(lz3),fil
		if 'j4' in fil:
			file=open(filename)
			lt=getfile(file)
			lj4=getkey(lt)
			print ' '.join(lj4),fil
		if 'm4m4' in fil:
			file=open(filename)
			lt=getfile(file)
			lm4=getkey(lt)
			print len(lm4),' '.join(lm4),fil
		if 'z4' in fil:
			file=open(filename)
			lt=getfile(file)
			lz4=getkey(lt)
			print len(lz4),' '.join(lz4),fil

	mj3=getoverlap(lj3,lm3)
	mz3=getoverlap(lz3,lm3)
	mj4=getoverlap(lj4,lm4)
	mz4=getoverlap(lz4,lm4)
	return [mj3,mz3,mj4,mz4]

def main():
	re=getall()
	print re

path='../result/'
main()
print 'finshed'	
			
