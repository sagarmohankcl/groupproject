#import socket
from socket import *

HOST = '' #localhost
PORT = 8000

print "Program running...1"

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)  # how many connections it can receive at one time
conn, addr = s.accept()  # accept the connection
print 'Connected by' , addr  # print address of the client connected

while True:
	data = conn.recv(1024) # 1024 bytes of data it can receive
	print "Received", repr(data)  # print data (message sent by client)
	reply = raw_input("Reply: ")
	conn.sendall(reply) # sends reply to every node connected

print "Program running...2"
conn.close()
