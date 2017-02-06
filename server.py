#synmolia chat server web 

import sys 
import socket 
import select

HOST = '' #localhost,otherwise change to IP address server is running on
socketList = []
buf = 4096
PORT = 8080 #default


#function to run server
def chat_server():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen(10)
	socketList.append(s) #adds server to list of available connections

#starting server

	while 1:
		#consider lists ready to be read and written to selection 
		read,write,error=select.select(socketList,[],[],0)
		#to read
		for sock in read:
			if sock == s:
				conn,addr = s.accept()
				socketList.append(conn)
				#print "someone has connected to the chat" %addr
				#client is connected
				broadcast(s,conn,"someone has joined the chatroom\n")

			else:
				try:
					#receiving data from socket
					data = sock.recv(buf)
					if data:
						print "["+str(sock.getpeername())+"]"+" > "+data
						#make broadcast of the remote address to which the socket is connected. 
						broadcast(s,sock,"\r" + '[' + str(sock.getpeername()) + ']' + data)
					else:
						if sock in socketList:
							socketList.remove(sock)
						broadcast(s,sock,"went offline"%addr)
				except:
					broadcast(s,sock,"is offline" %addr)
					continue

	s.close()
#make broadcast to every client that is connected on the 
def broadcast(s,sock,message):
	for socket in socketList:
		if socket != s and socket != sock:
			try:
				socket.send(message)
			except:
				socket.close()
				if socket in socketList:
					socketList.remove(socket)





if __name__ == "__main__":

	sys.exit(chat_server())





