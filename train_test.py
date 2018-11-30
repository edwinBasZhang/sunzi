#-*- coding:utf-8 -*-
import random

#sort -R result.txt -o last.txt

file_object_train = open('./train.txt','w')
file_object_test = open('./test.txt','w')
file_object = open('./last.txt','r') 
count = 0
for lines in file_object.readlines():
	if(count<=6376622):
        	file_object_train.write(lines)
                count = count + 1
        else:
                file_object_test.write(lines)
                count = count + 1
file_object_train.close()
file_object_test.close()

#file_object_train = open('./fp_apri_train.txt','w')
#file_object_test = open('./fp_apri_test.txt','w')
#file_object = open('./logfile.data','r')
#count = 0
#for lines in file_object.readlines():
#        if(count<=69999):
#                file_object_train.write(lines)
#                count = count + 1
#        else:
#                file_object_test.write(lines)
#                count = count + 1
#file_object_train.close()
#file_object_test.close()
