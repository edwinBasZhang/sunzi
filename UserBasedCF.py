#-*- coding:utf-8 -*-
import math

class UserBasedCF:
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
	
	def UserSimilarity_IIF(self,train=None):  
    		# input trainSet is a dict, for example:  
    		# train = {'A':{'a':rAa, 'b':rAb, 'd':rAd}, 'B':{...}, ...}  
    		# build the inverse table for item_users  
    		self.item_users_table = dict()  
    		for user, items in self.train.items():  
        		for item in items.keys():  
            			if item not in self.item_users_table:  
                			self.item_users_table[item] = set()  
            			self.item_users_table[item].add(user)  
    		# calculate co-rated items between users  
    		# item_users_table = {'a':set('A','B'), 'b':set('A','C'), ...}  
    		C = dict() # this is the member of W  
    		N = dict()   
    		for item, users in self.item_users_table.items():  
        		for uu in users: 
        			N.setdefault(uu,0) 
            			N[uu] += 1  
            			C.setdefault(uu,{})
            			for vv in users:  
                			if uu == vv:  
                    				continue  
                			## simple cosine user similarity  
                			C[uu].setdefault(vv,0)
                			C[uu][vv] += 1  
                			## modified cosine user similarity  
                			C[uu][vv] += 1 / math.log(1.0+len(item))  
    		# calculate final similarity matrix W  
    		self.W = dict()    
    		for uu, related_user in C.items():  
    			self.W.setdefault(uu,{})
        		for vv, Cuv in related_user.items():  
            			self.W[uu][vv] = Cuv / math.sqrt(N[uu]*N[vv])  
    		return self.W  

	def UserSimilarity(self,train=None):
		self.item_users=dict()

		for user,items in self.train.items():
			for i in items.keys():
				if i not in self.item_users:
					self.item_users[i]=set()
				self.item_users[i].add(user)
			#for k,v in item_users.items():
				#print k
				#print v

		C=dict()
		N=dict()

		for i,users in self.item_users.items():
			for u in users:
				N.setdefault(u,0)
				N[u]+=1

				C.setdefault(u,{})
				for v in users:
					if u ==v:
						continue
					C[u].setdefault(v,0)
					C[u][v]+=1

		self.W=dict()
		for u,related_users in C.items():
			self.W.setdefault(u,{})
			for v,cuv in related_users.items():
				self.W[u][v]=cuv/math.sqrt(N[u]*N[v])
		return self.W

	def Recommend(self,user,train=None,k=8,nitem=10):
		rank=dict()
		action_item=self.train[user].keys()
		
		for v,wuv in sorted(self.W[user].items(),key=lambda x:x[1],reverse=True)[0:k]:
			for i,rvi in self.train[v].items():
				if i in action_item:
					continue
				rank.setdefault(i,0)
				rank[i]+=wuv*rvi
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
	cf = UserBasedCF('./train.txt','./test.txt')
	cf.UserSimilarity()
	print "usercf"
	print("%3s%20s%20s%20s" % ('K', "recall", 'precision', 'popularity'))
        for k in [1,2,3,4,5, 10, 20, 40, 80, 160,180,200,220,240,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,280,300]:
                #k=10
                #print "111111111"
                #k = 5
                recall, precision = cf.recallAndPrecision(k=k)
                #print "222222222"
                #coverage = cf.coverage(k=k)
                #print "333333333"
                popularity = cf.popularity(k=k)
                #print "444444444"
                #print("%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, coverage * 100, popularity))
                print("%3d%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, popularity))
	cf.UserSimilarity_IIF()
	#print("%3s%20s%20s%20s%20s" % ('K', "recall", 'precision', 'coverage', 'popularity'))
	print "usercf-IIF"
	print("%3s%20s%20s%20s" % ('K', "recall", 'precision', 'popularity'))
	for k in [1,2,3,4,5, 10, 20, 40, 80, 160,180,200,220,240,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,280,300]:
        	#k=10
		#print "111111111"
		#k = 5
        	recall, precision = cf.recallAndPrecision(k=k)
		#print "222222222"
        	#coverage = cf.coverage(k=k)
		#print "333333333"
        	popularity = cf.popularity(k=k)
		#print "444444444"
        	#print("%3d%19.3f%%%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, coverage * 100, popularity))
		print("%3d%19.3f%%%19.3f%%%20.3f" % (k, recall * 100, precision * 100, popularity))
	#print cf.Recommend('479')
	b = raw_input("please input recommand id:")
	a = cf.Recommend(b)
	print a