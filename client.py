import sys 
import socket
import select

def chat_client():
	HOST = ''
	try:
		PORT = 8080
	except:
		print "not a valid port"
		sys.exit("you have exited the chat")


	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(2)

	try:
		s.connect((HOST,PORT))
	except:
		print"impossible connection"
		sys.exit()

	print "remote connection"
	uname = raw_input("Enter a username: ")
	sys.stdout.write("Your message: ") ; sys.stdout.flush()

	while 1:
		socket_list = [sys.stdin, s]
		read,write,error_sockets = select.select(socket_list,[],[])

		for sock in read:
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print "disconnected chat"
					sys.exit()
				else:
					sys.stdout.write(data)
					sys.stdout.write("Your message: " );sys.stdout.flush()
			else:
				msg = sys.stdin.readline()
				s.send(msg)
				sys.stdout.write("Your message: ");sys.stdout.flush()

if __name__ == "__main__":
	sys.exit(chat_client())

