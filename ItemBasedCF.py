#-*- coding:utf-8 -*-
import math

class ItemBasedCF:
	def __init__(self,train_file,test_file):
		self.train_file=train_file
		self.test_file=test_file
		self.readData()
	def readData(self):
		self.train=dict()
		for line in open(self.train_file):
			user,item,score=line.strip().split("\t")
			self.train.setdefault(user,{})
			self.train[user][item]=int(score)
		self.test=dict()
		for line in open(self.test_file):
			user,item,score=line.strip().split("\t")
                        self.test.setdefault(user,{})
                        self.test[user][item]=int(score)

	def ItemSimilarity_IUF(self,train=None):  
    		# calculate co-rated users between items  
    		C = dict()  
    		N = dict()  
    		for user,items in self.train.items():  
        		for ii in items.keys():  
        			N.setdefault(ii,0)
            			N[ii] += 1 
            			C.setdefault(ii,{}) 
            			for jj in items.keys():  
                			if ii == jj:  
                    				continue  
                			## the simple cosine item similarity 
                			C[ii].setdefault(jj,0) 
                			C[ii][jj] += 1  
                			## the modified cosine item similarity  
                			C[ii][jj] += 1 / math.log(1.0+len(user))  
    		# calculate final similarity matrix W  
    		self.W = dict()    
    		for ii, related_items in C.items():  
    			self.W.setdefault(ii,{})
        		for jj, Cij in related_items.items():  
            			self.W[ii][jj] = Cij / math.sqrt(N[ii]*N[jj])  
    		return self.W  

	def ItemSimilarity(self,train=None):
		C=dict()
		N=dict()
		for user,items in self.train.items():
			for i in items.keys():
				N.setdefault(i,0)
				N[i]+=1
				C.setdefault(i,{})
				for j in items.keys():
					if i==j:continue
					C[i].setdefault(j,0)
					C[i][j]+=1
			print user
			print items.keys()
			print "\r\n"
		self.W=dict()
		for i,related_items in C.items():
			self.W.setdefault(i,{})
			for j,cij in related_items.items():
				self.W[i][j]=cij/(math.sqrt(N[i]*N[j]))
		return self.W
	def Recommend(self,user,train=None,k=8,nitem=10):
		rank=dict()
		action_item = self.train[user]
		#print "action_item"
		#print action_item
		for item,score in action_item.items():
			for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:k]:
				if j in action_item.keys():
					continue
				rank.setdefault(j,0)
				rank[j] += score*wj
				#rank[j] += wj
		return sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:nitem]
	

	
	def recallAndPrecision(self, train=None, test=None, k=8, nitem=10):  
        	train = train or self.train  
        	test = test or self.test  
       		hit = 0  
        	recall = 0  
        	precision = 0  
        	for user in train.keys():  
            		tu = test.get(user, {})  
            		rank = self.Recommend(user,train,k=k, nitem=nitem)  
			#print "rank"
			#print rank
			rank = dict(rank)
            		for item,_ in rank.items():  
                		if item in tu:  
                    			hit += 1  
            		recall += len(tu)  
            		precision += nitem  
        	return (hit / (recall * 1.0), hit / (precision * 1.0))  
	def coverage(self, train=None, test=None, k=8, nitem=40):  
        	train = train or self.train  
        	test = test or self.test  
        	recommend_items = set()  
        	all_items = set()  
        	for user in test.keys():  
            		for item in test[user].keys():  
                		all_items.add(item)  
            		#rank = self.Recommend(user,train,k=k, nitem=nitem)  
            		for user in train.keys():  
                		for item in self.Recommend(user,train,k=k,nitem=nitem):  
                    			recommend_items.add(item)  
        	return len(recommend_items) / (len(all_items) * 1.0)  
    	def popularity(self, train=None, test=None, k=8, nitem=10):  
        	train = train or self.train  
        	test = test or self.test  
        	item_popularity = dict()  
        	for user, items in train.items():  
            		for item in items.keys():  
                		item_popularity.setdefault(item, 0)  
                		item_popularity[item] += 1  
        	ret = 0  
        	n = 0  
        	for user in train.keys():  
            		rank = self.Recommend(user,train,k=k, nitem=nitem)  
			rank = dict(rank)
            		for item, _ in rank.items():  
                		ret += math.log(1 + item_popularity[item])  
                		n += 1  
        	return ret / (n * 1.0)  

if __name__=='__main__':
	cf=ItemBasedCF('./train.txt','./test.txt')
	cf.ItemSimilarity()
	#cf.ItemSimilarity_IUF()
	#print("%3s%20s%20s%20s%20s" % ('K', "recall", 'precision', 'coverage', 'popularity')) 
	#print "itemcf算法"
	#print("%3s%20s%20s%20s" % ('K', "recall", 'precision', 'popularity'))
	#for k in [1,2,3,4,5, 10, 20, 40, 80, 160,180,200,220,240,260,280,300]:  
        	#k=10
		#print "111111111"
		#k = 5  
        	#recall, precision = cf.recallAndPrecision(k=k)
		#print "222222222"  
        	#coverage = cf.coverage(k=k)
		#print "333333333"  
        	#popularity = cf.popularity(k=k)
		#print "444444444"  
        	#print("%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, coverage * 100, popularity))  
		#print("%3d%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, popularity))
        cf.ItemSimilarity_IUF()
        #print("%3s%20s%20s%20s%20s" % ('K', "recall", 'precision', 'coverage', 'popularity'))
	#print "itemcf_iuf"
        #print("%3s%20s%20s%20s" % ('K', "recall", 'precision', 'popularity'))
        #for k in [1,2,3,4,5, 10, 20, 40, 80, 160,180,200,220,240,260,280,300,320,340,360,380,400]:
                #k=10
                #print "111111111"
                #k = 5
                #recall, precision = cf.recallAndPrecision(k=k)
                #print "222222222"
                #coverage = cf.coverage(k=k)
                #print "333333333"
                #popularity = cf.popularity(k=k)
                #print "444444444"
                #print("%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, coverag$
                #print("%3d%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, popularity))
	#print cf.Recommend('479')
	b = raw_input("please input recommand id:")
	a = cf.Recommend(b)
	print "aaaaaaaaaaaaaaaaaaa"
	print a