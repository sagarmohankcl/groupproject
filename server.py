#import socket
from socket import *
from threading import Thread


def clientHandler():
	conn,addr = s.accept()
	print addr, "is Connected"
	while 1:
		data = conn.recv(1024)
		if not data:
			break
		print "Recieved Message",repr(data)
		s.sendall(data)


HOST = '' #localhost
PORT = 8000

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)  # how many connections it can receive at one time
#conn, addr = s.accept()  # accept the connection
#print 'Connected by' , addr  # print address of the client connected
print "Program running...1"

for i in range(5):
	Thread(target=clientHandler().start())
# while True:
# 	data = conn.recv(1024) # 1024 bytes of data it can receive
# 	print "Received", repr(data)  # print data (message sent by client)
# 	reply = raw_input("Reply: ")
# 	conn.sendall(reply) # sends reply to every node connected

s.close()
