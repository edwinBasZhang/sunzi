import socket
import redis
HOST,PORT='',8888
listen_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
listen_socket.bind((HOST,PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...'%PORT
r2=redis.Redis(host="127.0.0.1",port=6380,db=0)

click_action={}

def gp(uid):
	file=open("./logfile.txt")
	for line in file.readlines():
		ls=line.strip().split("&")
		if ls[7]!="1":
			continue
		#print ls[1] + "\t" +ls[4]
		if ls[1] not in click_action.keys():
			click_action[ls[1]]=[]
		click_action[ls[1]].append(ls[4])
	if uid in click_action.keys():
		return "&&".join(click_action[uid])


comment_log={}

def log_process(line):
	print line
	request=line.strip()
	ls=request.split("&")
	if ls[1] not in comment_log.keys():
		comment_log[ls[1]]=[]
	comment_log[ls[1]].append(ls[4])
	for k,v in comment_log.items():
		print k+ "\t" + "&&".join(v)
	return "yes,i got it"


#pre_process
#file = open("./cate.log")
#cate_its={}
#for line in file.readlines():
#	line=line.strip()
#	ls = line.split("\t")
#	if ls[0] not in cate_its.keys():
#		cate_its[ls[0]] = []
#	lss = ls[1].split("&&")
#	for v in lss:
#		cate_its[ls[0]].append(v)
#for k,v in cate_its.items():
#	print k+ "\t" + "&&".join(v)
	

#tag=1 chinese
#tag=2 number
def log_process_one(request,tag):
	if tag == 1:
		if request in cate_its.keys():
			return "&&".join(cate_its[request])
		else:
			return "wrong request!"		
	elif tag == 2:
		for k,v in cate_its.items():
			if request in v:
				#return request + "#special" + "&&".join(v)
				return v[0] + "#special#" + request + "&&" + "&&".join(v)[1:]
		return "wrong request" 
	else:
		return "wrong"	

class RTR():
	old=["1","2","3","4","5"]
	new=["5","4","3","2","1"]
	def p(self,key):
		m=r2.get("9527#1")		
		if m != None:
			#if int(m) > 5000:
				#return "more than 5000"
			#else:
				#return "less than 5000"
			return  ",".join(self.new)
		else:
			return ",".join(self.old)


class App():
	app={}
	related={}
	related_fp={}
	def __init__(self):
		file = open('./train.txt')
		#print "read lines---------------"
		#for line in file.readlines():
				#print line
		#print "read lines---------------"
		for line in file.readlines():
			#print line
			ls = line.split("|")
			#print "-------------------"
			#print ls[1:]
			self.app[ls[0]]="&&".join(ls[1:])
			#print self.app[ls[0]]
			#print "--------------------"
		file = open("./result_apriori")
		for line in file.readlines():
			print line
			ls = line.strip().split("&&")
			self.related[ls[0]]="&&".join(ls[1:])
			print "**********************"
			print self.related[ls[0]]
			print "&&".join(ls[1:])
		file = open("./result_fpGrowth")
                for line in file.readlines():
                        ls = line.strip().split("&&")
                        self.related_fp[ls[0]]="&&".join(ls[1:])
	def check(self,appId):
		if appId in self.app.keys():
			return self.app[appId]

			#m = self.app[appId].split("&&")
			#ret=""
			#for i in range(0,len(m)):
			#	if i < 3:
			#		ret  += m[i] 
			#		ret += "\t"
			#	if i == 3:
			#		if m[i]== "0":
			#			ret += "noAction"
			#			ret +="\t"
			#		else:
			#			ret += "action"
			#			ret += "\t"
			#	if i == 4:
            #                           if m[i]== "0":
            #                                    ret += "noAdventure"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "adventure"
            #                                    ret += "\t"
			#	if i == 5:
            #                            if m[i]== "0":
            #                                    ret += "noAnimation"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "animation"
            #                                    ret += "\t"
			#	if i == 6:
            #                            if m[i]== "0":
            #                                    ret += "noChildren's"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "children's"
            #                                    ret += "\t"
			#	if i == 7:
            #                            if m[i]== "0":
            #                                    ret += "noComedy"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "comedy"
            #                                    ret += "\t"
			#	if i == 8:
            #                            if m[i]== "0":
            #                                    ret += "noCrime"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "crime"
            #                                    ret += "\t"
			#	if i == 9:
            #                            if m[i]== "0":
            #                                    ret += "noDocumentary"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "documentary"
            #                                    ret += "\t"				
			#	if i == 10:
            #                            if m[i]== "0":
            #                                    ret += "noDrama"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "drama"
            #                                    ret += "\t"
			#	if i == 11:
            #                            if m[i]== "0":
            #                                    ret += "noFantasy"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "fantasy"
            #                                    ret += "\t"
			#	if i == 12:
            #                            if m[i]== "0":
            #                                    ret += "noFilm-Noir"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "Film-Noir"
            #                                    ret += "\t"
			#	if i == 13:
            #                            if m[i]== "0":
            #                                    ret += "noHorror"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "horror"
            #                                    ret += "\t"
			#	if i == 14:
            #                            if m[i]== "0":
            #                                    ret += "noMusical"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "musical"
            #                                    ret += "\t"
			#	if i == 15:
            #                            if m[i]== "0":
            #                                    ret += "noMystery"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "mystery"
            #                                    ret += "\t"
			#	if i == 16:
            #                            if m[i]== "0":
            #                                    ret += "noRomance"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "romance"
            #                                    ret += "\t"
			#	if i == 17:
            #                            if m[i]== "0":
            #                                    ret += "noSci-Fi"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "Sci-Fi"
            #                                    ret += "\t"
			#	if i == 18:
            #                            if m[i]== "0":
            #                                    ret += "noThriller"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "thriller"
            #                                    ret += "\t"
			#	if i == 19:
            #                            if m[i]== "0":
            #                                    ret += "noWar"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "war"
            #                                    ret += "\t"
			#	if i == 20:
            #                            if m[i]== "0":
            #                                    ret += "noWestern"
            #                                    ret +="\t"
            #                            else:
            #                                    ret += "western"
            #                                    ret += "\t"

			#return ret					

		return "not found"
	def find_related(self,appId):
		if appId in self.related.keys():
			return self.related[appId]
		return "related not found"
	def detail(self,appId):
		ret = ""
		if appId in self.related.keys():
			ids = self.related[appId].split("&&")
			for idss in ids:
				ret += self.check(idss)
				ret += "\r\n"
		return ret	
	def detail_fp(self,appId):
		ret = ""
                if appId in self.related_fp.keys():
                        ids = self.related_fp[appId].split("&&")
                        for idss in ids:
                                ret += self.check(idss)
                                ret += "\r\n"
                return ret
		print ret
	


while True:
	client_connection,client_address = listen_socket.accept()
	request=client_connection.recv(1024)
	#http_response=gp(request)
	#http_response=log_process(request)
	#http_response=log_process_one(request,1)
	paras,tag = request.split("&&")
	#c = CutIndex()
	#http_response=c.read(paras)
	#r=RTR()
	#http_response=r.p(paras)
	m=App()
	http_response = m.detail(paras)
	#http_response = m.detail_fp(paras)
	#http_response=m.check(paras)
	#http_response=log_process_one(paras,int(tag))
	#http_response=log_process_one(request,2)
	client_connection.sendall(http_response)
	client_connection.close()

