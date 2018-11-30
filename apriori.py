#-*- coding:utf-8 -*-
from numpy import *

def loadDataSet():
	return [[1,3,4],
		[2,3,5],
		[1,2,3,6],
		[2,5],
		[2,3,5,6],
		[2,3,6],
		[3,6]]


def loadUseful():
	file=open("./train.txt")
	middle = {}
	ret = []
	for line in file.readlines():
		uid,mid,_,_ = line.split('\t')
		if uid not in middle.keys():
			middle[uid]=[]
		middle[uid].append(int(mid))
	print middle.values()[:5]
	return middle.values()[:5]

def createC1(dataSet):
	C1=[]
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	return map(frozenset,C1)

def scanD(D,Ck,minSupport):
	ssCnt={}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if not ssCnt.has_key(can):
					ssCnt[can]=1
				else:
					ssCnt[can]+=1
	numItems=float(len(D))
	retList=[]
	supportData={}
	for key in ssCnt:
		support = ssCnt[key]/numItems
		if support >=minSupport:
			retList.insert(0,key)
		supportData[key]=support
	return retList,supportData
			
def aprioriGen(Lk,k):
	#print "function aprioriGen"
	#print "Lk"
	#print Lk
	#print "k"
	#print k
	retList=[]
	lenLk=len(Lk)
	#print "lenLk"
	#print lenLk
	for i in range(lenLk):
		for j in range(i+1,lenLk):
			#print list(Lk[i])
			#print k-2
			L1=list(Lk[i])[:k-2]
			#print L1
			#print "Lk[j]"
			#print list(Lk[j])
			L2=list(Lk[j])[:k-2]
			#print "L2"
			#print L2
			#print "&&&&sort&&&&"
			#print L1.sort()
			#print L2.sort()
			if L1==L2:
				retList.append(Lk[i] | Lk[j])
	return retList
	

def apriori(dataSet,minSupport):
	#print "function apriori"
	C1=createC1(dataSet)
	D=map(set,dataSet)
	L1,supportData=scanD(D,C1,minSupport)
	#print "each element of L1"
	#for ll in L1:
		#print ll
		#print list(ll)
	L=[L1]
	k=2
	while(len(L[k-2])>0):
		#print "-----"
		#print k
		#print k-2
		#print L[k-2]
		#print L
		Ck=aprioriGen(L[k-2],k)
		#print "CK"
		#print Ck
		Lk,supK = scanD(D,Ck,minSupport)
 		#print "support K"
		#print supK
		supportData.update(supK)
		L.append(Lk)
		k+=1
	return L,supportData

def generateRules(L,supportData,minConf=0.7):
	bigRuleList=[]
	for i in range(1,len(L)):
		for freqSet in L[i]:
			H1=[frozenset([item]) for item in freqSet]
			#print "H1"
			#print H1
			#print "iiiiiiiiiiii"
			#print i
			if(i>1):
				#print "fuck you one"
				rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
			else:
				calcConf(freqSet,H1,supportData,bigRuleList,minConf)
	return bigRuleList
				


def calcConf(freqSet,H,supportData,brl,minConf=0.7):
	prunedH=[]
	for conseq in H:
		conf = supportData[freqSet]/supportData[freqSet-conseq]
		#print "support"
		#print supportData
		#print "support fuaak"
		#print freqSet-conseq
		#print supportData[freqSet-conseq]
		if conf>=minConf:
			#brl.append((freqSet-conseq,conseq,conseq,conf))
			brl.append((freqSet-conseq,conseq,conf))
			prunedH.append(conseq)
	return prunedH

def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
	m=len(H[0])
	#print "HHHH"
	#print H
	#1,2-->3,4
	#1,3-->2,4
	#1,4-->2,3
	#2,3-->1,4
	#2,4-->1,3
	#3,4-->1,2
	if (len(freqSet)>(m+1)):
		#Hmp1=[[1,2,3],[1,2,4],[1,3,4],[2,3,4]]
		Hmp1=aprioriGen(H,m+1)
		Hmp1=calcConf(freqSet,Hmp1,supportData,brl,minConf)
		if (len(Hmp1)>1):
			rulesFromConseq(freqSet,Hmp1,supportData,brl,minConf)




if __name__ =="__main__":
	#dataSet=loadDataSet()
	#print len(dataSet)
	dataSet=loadUseful()
	print len(dataSet)
  	support = input("please input support:")
	L,supportData=apriori(dataSet,support)
	#print "------------------------------------------"
	#print dataSet
	#print "------------------------------------------"
	#print supportData
	#print "*****************************************"
	#rules=generateRules(L,supportData,minConf=0.001)
	file=open("./result_apriori","w")
	for l in L:
		print l
		li=[]
		for ll in l:
			for k in ll:
				li.append(str(k))
		file.write("&&".join(li)+"\r\n")
		print ll
	file.close()
	#print "rules"
	#print "+++++++++++++++++++++++++++++++++++++++++"
	#print rules
	#print "+++++++++++++++++++++++++++++++++++++++++"
		
	#mushDatSet = [line.split() for line in open('mushroom.dat').readlines()]
	#L,supportData=apriori(mushDatSet,minSupport)

	#for item in L[3]:
		#if item.intersection('2'):
			#print item
