#-*- coding:utf-8 -*-
import socket
import os

ss =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.connect(('127.0.0.1',8888))
a = input("please input userid&&userid:")
ss.sendall(a)
os.system('sleep 1')
ss.send('EOF')
data = ss.recv(1024)
print "server's response:  %s"%data
file = open("./last_result_in.txt","w")
file.write(data)
file.close()
ss.close()
in_file = open("./last_result_in.txt","r")
out_file = open("./last_result_fp_middle.txt","wb")
for line in in_file:
	line = line.split("\r\n")
	for i in line:
		#print i
		i = i.split("&&")
		#print i[0]
		last = i[0]
		out_file.write(last)
	out_file.write("\n")
out_file.close()

file = open("./last_result_fp_middle.txt","r")
last = open("./last_result_fp.txt","w")
for line in file.readlines():
	last.write(line)
last.close()
file.close()
