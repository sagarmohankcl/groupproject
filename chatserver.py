
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
import thread
import json
import sqlite3
import datetime


#-------------------------------------------------------------------------------------------------
#   Multithreaded TCP server, allows remote clients to register and chat with other remote clients
#-------------------------------------------------------------------------------------------------

class Chatserver(object):
    def __init__(self, host, port):
        'Initialise the instance with an IP address and port number'
        self.host = host
        self.port = port        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Create TCP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))  #Bind the socket (sock) to the host and port

#------------------------------------------------------------------------------
#   Listens for connections from clients and spawns a new thread
#------------------------------------------------------------------------------

    def listen(self):
        try:
            print('Chatserver listening on {}:{}'.format(self.host,self.port))
            self.sock.listen(10)
        except:
            print('Server not listening')
            #Need to put a break here
        while True:
            connected_client, client_address = self.sock.accept()
            #Need to log the IP address of the client (connection) at this stage
            #create a method to do it
            'Connection Times out after 60 secs'
            connected_client.settimeout(60)   
            'Call thread with the client_handler method'
            thread.start_new_thread(self.client_handler,(connected_client, client_address))
            print "Connected client ", '{}'.format(client_address)
            #print('{}'.format(connected_client))

#------------------------------------------------------------------------------
#   Handles the client connection depending on the client request
#------------------------------------------------------------------------------

    def client_handler(self, connected_client, client_address):       
        size = 1024
        details = {}
        while True:
            try:                
                received_data = connected_client.recv(size)
                received_dict = json.loads(received_data.decode('utf-8'))                
                ip,host = client_address
                
                if received_dict:
                    received_dict['CONNECTION'] = '{}:{}'.format(ip,host)
                    #print(received_dict)
                    result = self.check_options(received_dict['OPTION'], received_dict)       
                                        
                else:
                    raise error('No one to send data to :(')

                result = json.dumps(result).encode('utf-8')                
                connected_client.send(result)                
            except:
                connected_client.close()
                return False

#------------------------------------------------------------------------------
#   Checks the action the connected client wants to be taken
#------------------------------------------------------------------------------

    def check_options(self, option, received_dict):      
        if option == 'NEW_USER':            
            result = self.new_user(received_dict)
        elif option == 'LOGIN':
            result = self.login(received_dict)
        elif option == 'QUERY_USER':            
            result = self.query_user(received_dict)            
        elif option == 'UPDATE_USER':
            result = self.update_user(received_dict)
        elif option == 'SEARCH_USER':
            result = self.search_user(received_dict)
        elif option == 'ADD_USER':
            result = self.add_user(received_dict)
        elif option == 'GET_CONTACTS':
            result = self.get_contacts(received_dict)
        else:
            return 'INVALID COMMAND'        
        return result

#------------------------------------------------------------------------------
#   Adds a user to the chatserver database
#------------------------------------------------------------------------------

    def new_user(self, received_dict):
        user = received_dict["USER"].lower()
        print "Registering " + received_dict["USER"] + "..."
        dt = str(datetime.datetime.now())        
        try: 
            con = sqlite3.connect('chatserver.db')
            cur = con.cursor()
            print 'try insert'  
            cur.execute("INSERT INTO users VALUES (?,?,?,?)",(received_dict['USER'].lower(),
                                                              received_dict['PASSWORD'],
                                                              received_dict['CONNECTION'],
                                                              dt))        
            print received_dict['USER'] + "added to the database"  
            con.commit()      
        except:
            return False
        con.close()
        return True

#------------------------------------------------------------------------------
#   Logs in users
#------------------------------------------------------------------------------

    def login(self, received_dict):
        user = self.query_user(received_dict)
        if user['PASSWORD'] == received_dict['PASSWORD']: 
            print received_dict['USER'] + " logged in"       
            return self.update_user(received_dict)              
        else:
            return False
 
#-------------------------------------------------------------------------
#   Queries for a user in the chatserver database and fetches its details 
#-------------------------------------------------------------------------     

    def query_user(self, received_dict):
        details = {'USER':'','PASSWORD':'','CONNECTION':'','DATE':''}        
        con = sqlite3.connect('chatserver.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT username, password, connection, date FROM users where username = ?",
                        (received_dict['USER'].lower(),))
            for record in cur:
                details['USER'] = record[0]
                details['PASSWORD'] = record[1]
                details['CONNECTION'] = record[2]
                details['DATE'] = record[3]
        except:
            return False 
        con.close()        
        return details

#------------------------------------------------------------------------------
#   Updates the timestamp for the record 
#------------------------------------------------------------------------------       

    def update_user(self, received_dict):
        con = sqlite3.connect('chatserver.db')
        cur = con.cursor()
        dt = str(datetime.datetime.now())
        try:
            cur.execute("Update users set date = ?, connection = ? where username = ?",
                        (dt,
                         received_dict['CONNECTION'],
                         received_dict['USER'].lower()))
            con.commit()
        except:
            return False
        con.close()
        return True


#-----------------------------------------------------------------------------------
#    Searches for a user in the chatserver database and return details to the client
#-----------------------------------------------------------------------------------  

    def search_user(self, received_dict):
        details = {'USER':'','DATE':''} 
        con = sqlite3.connect('chatserver.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT username, connection, date FROM users where username = ?",
                        (received_dict['USER'].lower(),))
            for record in cur:
                details['USER'] = record[0]
                details['DATE'] = record[2]
        except:
            return False
        con.close()
        return details

#------------------------------------------------------------------------------
#    Adds a contact to the contacts table in chatserver database for a client
#------------------------------------------------------------------------------  

    def add_user(self, received_dict):
        username = received_dict['USER']
        contact_name = received_dict['CONTACT']
        try: 
            con = sqlite3.connect('chatserver.db')
            cur = con.cursor()
            #print 'try inserting contact'  
            cur.execute("INSERT INTO contacts VALUES (?,?)",(received_dict['USER'].lower(),
                                                              received_dict['CONTACT'].lower()))        
            #print 'inserted contact'  
            con.commit()      
        except:
            return False
        con.close()
        return True

#------------------------------------------------------------------------------
#    Returns contact list to client from contacts table in chatserver database
#------------------------------------------------------------------------------  

    def get_contacts(self, received_dict):
        details = [] 
        con = sqlite3.connect('chatserver.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT contact_name FROM contacts where username = ?",
                        (received_dict['USER'].lower(),))
            for record in cur:
                details.append(record[0])
        except:
            return False
        con.close()
        return details
 
#-------------------------------------------------------------------------------------
#    Create chatserver database for storing registered users and contacts of each user
#------------------------------------------------------------------------------------- 

def create_db():
    con = sqlite3.connect('chatserver.db')
    cur = con.cursor()
    cur.execute(""" CREATE TABLE users (username string primary key, password text, connection text, date text)""")
    cur.execute("""CREATE TABLE contacts (username string, contact_name string, primary key (username, contact_name))""")
    con.commit()
    con.close()

#------------------------------------------------------------------------------
#    Deletes database'
#------------------------------------------------------------------------------          
            
def delete_db():
    con = sqlite3.connect('chatserver.db')
    cur = con.cursor()
    cur.execute(""" DROP TABLE """)
    con.commit()
    con.close()

    

    

if __name__ == "__main__":
    #port = eval(input('Enter port number to use: '))
    Chatserver('',5001).listen()
    #create_db()
    #new_user('john','123','127.0.0.1:5098')
    #update_user('marc','128.0.0.1:8000')
    #print(Chatserver.query_user('marc'))  
    
    
    
    
