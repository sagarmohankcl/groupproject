'''
Group: Synomilia
Date:  2017-02-08
Description:
A multithreaded server class that listens for connections from on clients on the
Port specified and spawns a new connection to handle the client connection.

Consists of:
- Chatserver class
- Constructor Method. To initialise the Chatserver object with a host IP and port
- listen method. To listen for connections from clients
- Client_handler method. To 

'''

import socket
import threading

class Chatserver(object):
    'Multithreaded TCP server to allow clients to connect to chat to each other'

    def __init__(self, host, port):
        'Initialise the instance with an IP address and port number'
        self.host = host
        self.port = port        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Create TCP socket
        self.sock.bind((self.host, self.port))  #Bind the socket (sock) to the host and port


    def listen(self):
        'Listens for connections from clients and spawns a new thread'
        print('Server listening on {}:{}'.format(self.host,self.port))
        self.sock.listen(10)    
        while True:
            connected_client, client_address = self.sock.accept()
            #Need to log the IP address of the client (connection) at this stage
            #create a method to do it
            'Connection Times out after 60 secs'
            connected_client.settimeout(60)   
            'Call thread with the client_handler method'
            threading.Thread(target = self.client_handler, args = (connected_client, client_address)).start()


    def client_handler(self, connected_client, client_address):
        'Handles the client connection depending on the client request'
        'For now the method echos the client data back to them, for testing purposes'
        size = 1024
        while True:
            try:
                received_data = connected_client.recv(size)
                if received_data:
                    'Send back what the client sent'
                    sent_data = received_data
                    connected_client.send(sent_data)
                    'This is for testing, TAKEOUT!'
                    print(sent_data)
                else:
                    raise error('No one to send data to :(')
            except:
                connected_client.close()
                return False


if __name__ == "__main__":
    port = eval(input('Enter port number to use: '))
    Chatserver('',port).listen()
