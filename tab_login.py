import socket
import json
import threading
import thread
import queue
from tkinter import *
import tkinter as tk
from tkinter import ttk
import time


class Client(object):
    'Chat application Client'
    username = 'marc'
    password ='password'
    l =[]    
    user_tabs_list = {}
    user_send_list = {}
    'used to store list of tabs?'
    list_of_tabs = {}
    tab_name_user = {}
    'Use to store the mapping of users to socket connection'
    user_connection = {}
    received_messages = queue.Queue()     
    sent_messages = queue.Queue()
    name = ['mary','john','joe']
    chat_button_user =''

    options = {'login': {'OPTION':'LOGIN','USER':username,'PASSWORD':password},
               'query': {'OPTION': 'QUERY_USER','USER':username},
               'update': {'OPTION': 'UPDATE_USER','USER':username},
               'new' : {'OPTION':'NEW_USER','USER': username,'PASSWORD': password}
               }


    def __init__(self):
        'This method initialises the basic window'
        #self.received_messages = queue.Queue()
        #self.sent_messages = queue.Queue()
        self.window = Tk()
        self.window.title("Synomilia Chat")
        
        self.tab_controller = ttk.Notebook(self.window)
        
        self.login_tab()
        self.main_tab()
        thread.start_new_thread(self.local_server,())
        'Schedule gui_update to run on the main thread in one second'
        self.window.after(1000, self.gui_update)
        
        

    def main_tab(self):
        'This method contains the controls for the main tab'
        '''self.tab_controller.add(self.main, text='Main')
        self.tab_controller.pack(expand=1, fill="both")
        self.main_frame = ttk.LabelFrame(self.main, text=' Synomilia ')
        self.main_frame.grid(column=0, row=0, padx=8, pady=4)'''

        self.main = ttk.Frame(self.tab_controller)
        self.tab_controller.add(ttk.LabelFrame(width=500, height=550,text= ''),text= '')
        self.tab_controller.pack(expand=1, fill="both")
        #conversation_frame = ttk.LabelFrame(self.main, text=' Conversation ')
        #conversation_frame.grid(column=0, row=0, padx=8, pady=4)
        
        

    def chat_tab(self,name):
        'This method has the controls and calls the methods for the chat window'        
        tab_name = ttk.Frame(self.tab_controller,name=name)        
        self.tab_controller.add(tab_name, text= name)
        'uncomment if tab needs to be active when msg received'
        #self.tab_controller.select(tab_name) take out bottom too
        self.tab_name_user[tab_name] = name
        conversation_frame = ttk.LabelFrame(tab_name, text=' Conversation ')
        conversation_frame.grid(column=0, row=0, padx=8, pady=4)
        
        display = Text(conversation_frame, bg="white", width=60, height=30, name='display')
        display.grid(column=0, row=1, sticky='W')
        self.user_tabs_list[name] = display
        
        'Box to type message'
        submit_text = ttk.Entry(conversation_frame, width=60)
        submit_text.grid(column=0, row=2, padx=3, pady=5, ipady=5,sticky=W)
        'Send Button'
        send = ttk.Button(conversation_frame, text="Send")
        send.grid(column=0, row=2, padx=10,ipady=4, sticky=E)
        #check here - take out
        self.user_send_list[name] = submit_text
        send.bind("<Button-1>",self.chat_send_button)
        send.bind("<Return>",self.chat_send_button)


    def chat_send_button(self,event):
        'Gets the tab id, the calls the get_text method to update window'
        tab = self.tab_controller.select()
                
        for key in self.tab_name_user.keys():           
            if str(tab) ==  str(key):
                user = (self.tab_name_user.get(key))  
        self.get_text(user)


    def chat_connection(self,name):
        'Check if user is in the user_connection list'
        'If not it means that the conversation was initiated from the contact list'
        'initiate a connection to the user by add them to the list'
        'calling connect_remote_server method'
        'Check if a connection for the user exists'
        ###### turn this into a function that the contacts message button calls
        ####then call the chat tab from this function
        
        if name not in self.user_connection.keys():            
            
            'Query the user to get connection details'
            self.options['query']['USER'] = name
            results = (self.connect_remote_server(self.options['query']))            
            if results['CONNECTION'] != '':
                host,port = results['CONNECTION'].split(':')
                'Connect to the remote client and get the socket information'
                'Store name and socket details in global list'
                connected_client = self.connector(host,port)
                self.user_connection[name] = connected_client
                print('tuesday')
                
            else:
                print('User is not online')
                ####Put a pop up window here
                #update client sock list after connect

    def connector(self, host,port):
        'Method to initiate TCP connection to client'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msg = '{} started a chat...'.format(self.username)
        data = {'USER': 'marc','MSG':msg}        
        data = json.dumps(data).encode('utf-8')
        
        'Start the connection and send initial message'
        sock.connect((host, port))
        sock.send(data)
        'Start thread to receive messages'
        'Can take out host but need to modify the method below'
        thread.start_new_thread(client_handler,(sock, host))
        return sock
                

        

    def contacts_tab(self):
        'Displays the tab with contacts'
        self.contacts = ttk.Frame(self.tab_controller, name='contacts')
        self.tab_controller.add(self.contacts, text='Contacts')
        contacts_frame = ttk.Frame(self.contacts)
        contacts_frame.grid(column=0, row=0, padx=80, pady=4, columnspan=2, sticky='newss')

        'Add listbox to the frame'
        listbox_frame = ttk.Frame(self.contacts)
        listbox_frame.grid(column=0, row=0, padx=80, pady=10)
        contacts_listbox = ttk.Treeview(listbox_frame)
        contacts_listbox.grid(column=0,row=1, pady=4, ipadx=2, ipady=2, sticky='w')
        #Scroll bar need to check
        #list_scroll = ttk.Scrollbar(self.contacts)       
        #list_scroll.configure(command=contacts_listbox.yview)
        #contacts_listbox.configure(yscrollcommand=list_scroll.set)

        'Add Search'
        self.search_entry = ttk.Entry(listbox_frame)
        self.search_entry.grid(column=0, row=2, padx=1, pady=3,sticky='w')
        search_button = ttk.Button(listbox_frame, text='Search')
        search_button.grid(column=0,row=2,  sticky='e')
        search_button.bind("<Button-1>",self.contacts_search)
        search_button.bind("<Return>",self.contacts_search)

    def contacts_search(self,event):
        'Gets the text from the search field onthe login tab'
        'Calls the connect_remote server method'
        'Returns the result'
        results ={}
        user = self.search_entry.get()        
        self.chat_button_user = user
        if user != '':
            self.options['query']['USER'] = user            
            results = (self.connect_remote_server(self.options['query']))
            
            if results['CONNECTION']!= '':
                'Pop up window to notify the user'
                notify = Toplevel()
                notify.title('Search User')
                msg = Message(notify, text='User found',width=80)
                msg.pack()
                login_frame = ttk.Frame(notify)
                login_frame.pack()
                chat_button = ttk.Button(login_frame, text='Message User',width=15)
                chat_button.pack()
                chat_button.bind("<Button-1>",self.chat_button_clicked)
                contacts_add = ttk.Button(login_frame, text='Add Contact',width=15)
                contacts_add.pack()
                
                
            else:                
                'Pop up window to notify the user'
                notify = Toplevel()
                notify.title('Search User')
                msg = ttk.Label(notify, text='User not found')
                msg.pack()
            self.search_entry.delete(0,END)

    def chat_button_clicked(self,event):
        'Open a new chat tab'
        self.chat_tab(self.chat_button_user)
        self.chat_connection(self.chat_button_user)
        
        



    def login_tab(self):
        'Displays login Form '
        newuser_var = IntVar()        
        self.login = ttk.Frame(self.tab_controller, name='login')
        self.tab_controller.add(self.login, text= 'Login')
        login_frame = ttk.Frame(self.login)
        login_frame.grid(column=0, row=0, padx=80, pady=4)
        
        'Add Icon'
        login_icon_frame = ttk.Frame(self.login)
        login_icon_frame.grid(column=0,row=0,padx=75)
        login_icon = PhotoImage(file='chaticon.png')
        login_icon_label = Label(login_icon_frame, image=login_icon)
        login_icon_label.image = login_icon
        login_icon_label.grid(column=0,row=1,pady=15, sticky='w')

        'Add labels and buttons'
        credential_frame = ttk.LabelFrame(self.login, text='Login')
        credential_frame.grid(column=0,row=1,padx=85, pady=4, ipadx=2, ipady=2, sticky='w')

        username_label = ttk.Label(credential_frame, text='Username: ')
        username_label.grid(column=1, row=1, sticky=W)
        self.username_entry = ttk.Entry(credential_frame)
        self.username_entry.grid(column=2, row=1, pady=3,sticky=E)

        self.password_entry = ttk.Entry(credential_frame, show="*")
        self.password_entry.grid(column=2, row=2, pady=3,sticky=E)

        newuser_label = ttk.Label(credential_frame, text='New User:')
        newuser_label.grid(column=1, row=4, sticky='w')
        newuser_checkbutton = ttk.Checkbutton(credential_frame,
                                              variable=newuser_var,
                                              offvalue=0,
                                              onvalue=1)
        
        newuser_checkbutton.grid(column=2, row=4, sticky='w')
        password_label = ttk.Label(credential_frame, text='Password:')
        password_label.grid(column=1, row=2, sticky=W)
        
        
        submit_button = ttk.Button(credential_frame, text='Submit')
        submit_button.grid(column=2,row=4, columnspan=2, sticky='e')
        submit_button.bind("<Button-1>",self.login_submit)
        submit_button.bind("<Return>",self.login_submit)

    def login_submit(self,event):
        'Gets the text from the username and password field on the login tab'
        'Calls the connect_remote server method'
        'Hides the login tab'
        'Calls the Main tab'
        self.success = False
        username = self.username_entry.get()
        password = self.password_entry.get()        
        if username != '' and password != '':
            self.options['login']['USER'] = username
            self.options['login']['PASSWORD'] = password
            if self.connect_remote_server(self.options['login']):             
                self.contacts_tab()
                self.tab_controller.hide(self.login)             
            else:
                self.username_entry.delete(0,END)
                self.password_entry.delete(0,END)
                'Pop up window to notify the user'
                notify = Toplevel()
                notify.title('Failed Login')
                msg = Message(notify, text='Login Failed')
                msg.pack()
                      
            
                
                

    def gui_update(self):
        'Method called every second to update the window'
        #Might need to split the two trys in two methods'
        
        'Check the received_messages queue'        
        try:            
            received_message = self.received_messages.get_nowait()
            user = received_message['USER']
            msg = received_message['MSG']
            

            'Check if tab exists for user or not'
            'Create new tab or update existing tab'
            self.user_tabs_list
            if user not in self.user_tabs_list.keys():                    
                self.chat_tab(user)
                print(user, msg)
                self.update_window(user,msg)
                print(self.user_tabs_list)
                print('empty?')
            else:
                self.update_window(user,msg)
        except: #QueueEmpty: Need to find the exception to catch it here
            'Its ok if theres no data in the queue'
            'Will check again later'
            pass
        

        try:            
            sent_message = self.sent_messages.get_nowait()
            
            #call the send method now? or put this in the send method
            'Check to see if the user is in the user_connection list'            
            for key in self.user_connection.keys():           
                if sent_message['USER'] ==  str(key):
                    'Get the connection string'
                    print(sent_message)
                    connected_client = self.user_connection.get(key)                                
                    print(connected_client)                    
                    'encode the message as json and send'
                    self.send_message(sent_message, connected_client)                                                  
        except:
            'Its ok if theres no data in the queue'
            'Will check again later'
            pass
        
        'Schedule gui_update again in one second'        
        self.window.after(1000, self.gui_update)

        
        

    


    def connect_remote_server(self,data):
        'Login Method'
        HOST = '127.0.0.1'
        PORT = 5001             
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:     
            print(data)
            data = json.dumps(data).encode('utf-8')        
            s.connect((HOST, PORT))
            s.send(data)

            while True:
                data = s.recv(1024)            
                if data:
                    data = json.loads(data.decode('utf-8'))
                    return data
                else:
                    #check this line if other things are broken
                    return False

    #Use inheritance from the method above
    def connect_remote_client(self, host, port):
        'Method to connect to other clients'
        #data ={'USER': self.username, 'MSG':'Started a chat...'}
                     
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   
            print(s)
            data = json.dumps(data).encode('utf-8')        
            s.connect((host, port))            
            #thread.start_new_thread(self.remote_client_send,(s))
            #thread.start_new_thread(self.remote_client_recv,(s))

            """while True:
                data = s.recv(1024)            
                if data:
                    data = json.loads(data.decode('utf-8'))
                    return data
                else:
                    #check this line if other things are broken
                    return False"""


    def remote_client_send(self,sock):
        'Method to send data to the connected client'
        data ={'USER': self.username, 'MSG':'Started a chat...'}
        sock.send(data)
        print('remote client recv thread started')
        while True:
            try:            
                sent_message = self.sent_messages.get_nowait()
                sent_message = json.dumps(sent_message).encode('utf-8')         
                sock.send(sent_message)
            except:
                pass
            

    def remote_client_recv(self,connected_client):
        'Method to receive data from connected client'
        size = 1024
        print('remote client recv thread started')
        while True:
            received_data = connected_client.recv(size)
            if received_data:
                received_data = json.loads(received_data.decode('utf-8'))
                user = received_data['USER']
                self.user_connection[user] = connected_client
                self.received_messages.put_nowait(received_data)
    

    def local_server(self):
        'Initialise the instance with an IP address and port number'
        self.host = '127.0.0.1'#host
        self.port = 8080#port        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Create TCP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))  #Bind the socket (sock) to the host and port
    
        'Listens for connections from clients and spawns a new thread'
        try:
            print('Server listening on {}:{}'.format(self.host,self.port))
            self.sock.listen(10)
        except:
            print('Server not listening')
            #Need to put a break here
            
        while True:
            connected_client, client_address = self.sock.accept()
            #Need to log the IP address of the client (connection) at this stage
            #create a method to do it
            'Connection Times out after 60 secs'
            #connected_client.settimeout(120)   
            'Call thread with the client_handler method'
            thread.start_new_thread(self.client_handler,(connected_client, client_address))
            
            #thread.start_new_thread(self.client_handler2,(connected_client, client_address))
            
            print('{}'.format(client_address))
            print('{}'.format(connected_client))

            """size = 1024
            received_data = connected_client.recv(size)
            if not received_data:
                break
            received_data = json.loads(received_data.decode('utf-8'))
            user = received_data['USER']
            self.user_connection[user] = connected_client
            self.received_messages.put_nowait(received_data)
            connected_client.close()
           """ 
            #thread.start_new_thread(self.remote_client_recv,(connected_client))
            #thread.start_new_thread(self.remote_client_send,(connected_client))
            

            


    def client_handler(self,connected_client, client_address):
        'Send and receive data from each client that connects'        

        size = 1024
        result = ''
        #ip,host = client_address        
        
        while True:
            received_data = connected_client.recv(size)
            if not received_data:
                break
            received_data = json.loads(received_data.decode('utf-8'))
            user = received_data['USER']
            self.user_connection[user] = connected_client
            self.received_messages.put_nowait(received_data)
            print('Client Handler thread started...')
        connected_client.close()


    def client_handler2(self,connected_client, client_address):
        'Method to send data to the connected client'
        sent_message ={'USER': self.username, 'MSG':'Started a chat...'}
        sent_message = json.dumps(sent_message).encode('utf-8')
        size = 1024
        result = ''
        ip,host = client_address   
        connected_client.send(sent_message)
        print('Client Handler 2 thread started...')
        while True:
            try:            
                sent_message = self.sent_messages.get_nowait()
                sent_message = json.dumps(sent_message).encode('utf-8')         
                connected_client.send(sent_message)
                
            except:
                pass
            
            
                    
        
      
            
                
            
            
            
    def receive(self):
        'Method to receive data from to remote client'
        while True:
            if not self.received_messages.empty():
                print(self.received_messages.get_nowait())
        


    def send_message(self,sent_message, connected_client):
        'Method to send data to the connected clients'
        'First encode as json and then send'
        result= json.dumps(sent_message).encode('utf-8')        
        try:            
            #####Something here?
            connected_client.sendall(result)
            print('wednesday')
        except:
            print('unable to send the message: '.format(message))
        
        
    
    def main_window(self):
        'Create main chat window'
        self.root = Tk()
        
        
      
        self.root.mainloop()
        
    def chat_window(self):
        'GUI window to be used for chatting'
        self.window = Toplevel()
        self.remote_client =''
        
        #self.display = Text(self.window, state='disabled', bg="white", width=60, height=30)        
        self.display = Text(self.window, bg="white", width=60, height=30) 
        self.submit_text = Entry(self.window, width=50)        
        self.send = Button(self.window, text="Send",width=15, height=2)
        
        self.display.grid(row=0, column=0, sticky=W)
        self.submit_text.grid(row=1,column=0,padx=15,ipady=4,sticky=W)
        self.send.grid(row=1,column=0,sticky=E)

        self.send.bind("<Button-1>",self.mouse_enter)
        'Not sure why had to bind to root'
        self.window.bind("<Return>",self.mouse_enter)
        
        

    def update_window(self,user,message):
        'Add text to the display when enter or send is pressed'
        self.user_tabs_list[user].configure(state='normal')                
        self.user_tabs_list[user].insert(END,'{}: {}\n \n'.format(user,message))        
        self.user_tabs_list[user].configure(state='disabled')
        
        
        

    def get_text(self,user):
        'Check if submit_text not empty and return data'
        message =''
        sent_data = {}
        
        if self.user_send_list[user].get() != '':
            message = self.user_send_list[user].get()
            self.update_window(self.username,message)
            self.user_send_list[user].delete(0,END)
            sent_data['USER']= user
            sent_data['MSG'] = message
            
            'Add message to the outgoing queue'                
            self.sent_messages.put_nowait(sent_data)
            
            
            
        
            
        

    def mouse_enter(self,event):
        'Used by the send button to respond to mouse and enter key events'
        self.get_text()


    
        
        

def run():
        
    chat = Client()
    'Start mainloop'
    chat.window.mainloop()   
 
           
                       

if __name__ == "__main__":
    run()
    
