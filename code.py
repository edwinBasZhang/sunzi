import json
#encoding=utf8 
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

with open('last.json') as jsonfile:
	data = json.load(jsonfile)
	print(data)
	for count, line in enumerate(open('last.json','rU')):
		pass
	count+=1
	for i in range(count):
		print(i)
		print(data[i]["user_id"])
		result = data[i]["user_id"]
		name = data[i]["name"]
		rating = data[i]["review_count"]
		file = open('result.txt','a')
		file.write(result+'\t'+name+'\t'+str(rating)+'\r\n')
		file.close