import socket
import json
import threading
import thread
import Queue as queue
from Tkinter import *
#import tkinter as tk  fpr python 3 
#from tkinter 
from ttk import *
from PIL import Image, ImageTk
import time
import encrypt_password
from encrypt_password import *
import sqlite3
import os.path


class Client(object):
    'Chat application Client'
    username = ''
    password =''
    connection = ''
    l =[]    
    user_tabs_list = {}
    user_send_list = {}
    'used to store list of tabs?'
    tab_name_user = {}
    'Use to store the mapping of users to socket connection'
    user_connection = {}
    received_messages = queue.Queue()     
    sent_messages = queue.Queue()
    
    open_chat_tabs = {}
    contacts_dict = {} #{username:{'CONNECTION':connection,'TIME':time}} 

    options = {'login': {'OPTION':'LOGIN','USER':username,'PASSWORD':password},
               'query': {'OPTION': 'QUERY_USER','USER':username},
               'update': {'OPTION': 'UPDATE_USER','USER':username},
               'new' : {'OPTION':'NEW_USER','USER': username,'PASSWORD': password},
               'search': {'OPTION': 'SEARCH_USER', 'USER':username},
               'add' : {'OPTION': 'ADD_USER', 'USER':username, 'CONTACT': ''},
               'get': {'OPTION': 'GET_CONTACTS', 'USER':username}
               }
    

    def __init__(self):
        'This method initialises the basic window'
        self.master = Frame(name='general')
        self.root = self.master.master  # short-cut to top-level window
        self.master.pack()  # pack the Frame into root, defaults to side=TOP
        self.root.title('Synomilia Chat')  # name the window
        
        self.demoPanel = Frame(self.master, name='demo')  # create a new frame slaved to master
        self.demoPanel.pack()  # pack the Frame into root

        # create (notebook) demo panel
        self.tab_controller = Notebook(self.demoPanel, name='notebook',width=420, height=550)  # create the ttk.Notebook widget

        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        self.tab_controller.enable_traversal()
        self.tab_controller.pack(fill=BOTH, expand=Y, padx=2, pady=3)  # add margin

        self.login_tab() 
        thread.start_new_thread(self.local_server,())
        'Schedule gui_update to run on the main thread in one second'
        self.demoPanel.after(1000, self.gui_update)



#------------------------------------------------------------------------------
#   It opens the login tab
#------------------------------------------------------------------------------

    def login_tab(self):
        'Displays login Form '

        frame = Frame(self.tab_controller, name='login')

        newuser_var = IntVar()        
        self.login = Frame(self.tab_controller, name='login')
        self.tab_controller.add(self.login, text= 'Login')
        login_frame = Frame(self.login)
        login_frame.grid(column=0, row=0, padx=80, pady=4)
        
        'Add Icon'
        login_icon_frame = Frame(self.login)
        login_icon_frame.grid(column=0,row=0,padx=60, sticky='we')
        login_icon = ImageTk.PhotoImage(Image.open('chat-2-icon.png'))
        login_icon_label = Label(login_icon_frame, image=login_icon)
        login_icon_label.image = login_icon
        login_icon_label.grid(column=0,row=1,padx=10,pady=15, sticky='ew')

        'Add labels and buttons'
        self.credential_frame = LabelFrame(self.login, text='Login')#, height=50, width=100)
        self.credential_frame.grid(column=0,row=1,padx=105, pady=4, ipadx=2, ipady=2, sticky='w')

        username_label = Label(self.credential_frame, text='Username: ')
        username_label.grid(column=1, row=1, sticky=W)
        self.username_entry = Entry(self.credential_frame)
        self.username_entry.focus_set()
        self.username_entry.grid(column=2, row=1, pady=3,sticky=E)

        self.password_entry = Entry(self.credential_frame, show="*")
        self.password_entry.grid(column=2, row=2, pady=3,sticky=E)

        password_label = Label(self.credential_frame, text='Password:')
        password_label.grid(column=1, row=2, sticky=W)
                
        submit_button = Button(self.credential_frame, text='Submit')
        submit_button.grid(column=2,row=4, columnspan=2, sticky='e')
        submit_button.bind("<Button-1>",self.login_submit)
        submit_button.bind("<Return>",self.login_submit)

        register_button = Button(self.credential_frame, text='Register')
        register_button.grid(column=1,row=4, columnspan=2, sticky='w')
        register_button.bind("<Button-1>",self.register_newuser)
        register_button.bind("<Return>",self.register_newuser)

        self.alert_message = StringVar()
        self.alert_label = Label(self.credential_frame, textvariable=self.alert_message, foreground='red')
        self.alert_label.grid(columnspan=3)


#------------------------------------------------------------------------------
#   It connects to server and open contacts tab
#------------------------------------------------------------------------------

    def login_submit(self,event):
        'Gets the text from the username and password field on the login tab'
        'Calls the connect_remote server method'
        'Hides the login tab'
        'Calls the Main tab'
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()        
        if self.username != '' and self.password != '':
            self.options['login']['USER'] = self.username
            self.options['login']['PASSWORD'] = encrypt(self.password)
            if self.connect_remote_server(self.options['login']):             
                self.contacts_tab()
                self.tab_controller.hide(self.login)                
            else:
                self.alert_message.set('Username or password mismatching')
        else:
            self.alert_message.set('Username or password missing')
            


#------------------------------------------------------------------------------
#   It opens a pop up window for registration 
#------------------------------------------------------------------------------
    
    def register_newuser(self, event):
        'Open new window and allow registration of a new user'
        self.register_w = Toplevel()
        self.credential_frame_R = LabelFrame(self.register_w, text='Registration new user')
        self.credential_frame_R.grid(column=0,row=1,padx=85, pady=4, ipadx=2, ipady=2, sticky='w')

        username_label = Label(self.credential_frame_R, text='Username: ')
        username_label.grid(column=1, row=1, sticky=W)
        self.username_entry = Entry(self.credential_frame_R)
        self.username_entry.grid(column=2, row=1, pady=3,sticky=E)

        self.password_entry_1 = Entry(self.credential_frame_R, show="*")
        self.password_entry_1.grid(column=2, row=2, pady=3,sticky=E)

        password_label_1 = Label(self.credential_frame_R, text='Password:')
        password_label_1.grid(column=1, row=2, sticky=W)
        
        self.password_entry_2 = Entry(self.credential_frame_R, show="*")
        self.password_entry_2.grid(column=2, row=3, pady=3,sticky=E)

        password_label_2 = Label(self.credential_frame_R, text='Repeat password:')
        password_label_2.grid(column=1, row=3, sticky=W)    

        submit_button = Button(self.credential_frame_R, text='Submit')
        submit_button.grid(column=2,row=4, columnspan=2, sticky='e')
        submit_button.bind("<Button-1>",self.register_submit)
        submit_button.bind("<Return>",self.register_submit)
        self.tab_controller.hide(self.login)   # 


#------------------------------------------------------------------------------
#   It connects to server and open contacts tab
#------------------------------------------------------------------------------

    def register_submit(self,event):
        'Gets the text from the username and password field on the login tab'
        'Calls the connect_remote server method'
        'Close registration window'
        #'Hides the login tab'
        'Calls the Main tab'
        self.username = self.username_entry.get()
        password_1 = self.password_entry_1.get() 
        password_2 = self.password_entry_2.get() 

        if self.username != '' and password_1 != '' and (password_1 == password_2):
            self.password = password_1
            self.options['new']['USER'] = self.username
            self.options['new']['PASSWORD'] = encrypt(self.password)
            if self.connect_remote_server(self.options['new']):             
                self.contacts_tab()
                #self.tab_controller.hide(self.login)
                self.register_w.destroy()                
            else:
                self.username_entry.delete(0,END)
                self.password_entry_1.delete(0,END)
                'Pop up window to notify the user'   # make a label?-----------------
                notify = Toplevel()
                notify.title('Failed Registration')
                msg = Message(notify, text='Registration Failed')
                msg.pack()
        else:
            alert_label = Label(self.credential_frame_R, text='Username missing or password mismatching', foreground='red')
            alert_label.grid(columnspan=3)



#------------------------------------------------------------------------------
#   Main page of the app:
#------------------------------------------------------------------------------

    def contacts_tab(self):
        
        'Displays the tab with contacts'
        self.contacts = Frame(self.tab_controller, name='contacts')
        self.tab_controller.add(self.contacts, text='Contacts')
        contacts_frame = Frame(self.contacts)
        contacts_frame.grid(column=0, row=0, padx=4, pady=4, columnspan=2, sticky='newss')

        'Add Icon'
        contacts_icon_frame = Frame(self.contacts, width=180, height=180)
        contacts_icon_frame.grid(column=0,row=0)#,padx=75)
        #contacts_icon_frame.grid_propagate(False)

        #login_icon = PhotoImage(file='chaticon.png')
        contacts_icon = ImageTk.PhotoImage(Image.open('chat-2-icon_small.png'),width=5,height=5)
        contacts_icon_label = Label(contacts_icon_frame, image=contacts_icon, width=5)
        contacts_icon_label.image = contacts_icon
        contacts_icon_label.grid(column=0,row=1,pady=2, sticky='w')

        'Add listbox to the frame'
        listbox_frame = Frame(self.contacts)
        listbox_frame.grid(column=0, row=1, padx=100, pady=10)

        self.contacts_listbox = VerticalScrolledFrame(listbox_frame)
        self.contacts_listbox.grid(column=0,row=1, pady=4, ipadx=2, ipady=2, sticky='w')

        'Get previously added contacts and display'
        self.get_contacts()
        self.display_contacts()
        
        'Add Search'
        self.search_entry = Entry(listbox_frame)
        self.search_entry.grid(column=0, row=2, padx=1, pady=3,sticky='w')
        search_button = Button(listbox_frame, text='Add Contact')
        search_button.grid(column=0,row=2, sticky='e')
        search_button.bind("<Button-1>",self.contacts_search)
        search_button.bind("<Return>",self.contacts_search)

        'Label for communication about results'
        self.search_message = StringVar()
        self.search_label = Label(listbox_frame, textvariable=self.search_message, foreground='blue')
        self.search_label.grid(columnspan=3)

        'Add Logout Button'
        logout_frame = Frame(self.contacts,width=180, height=180)
        logout_frame.grid(column=0, row=2)#,padx=4, pady=4, columnspan=2)#, sticky='newss')
        logout_button = Button(logout_frame, text='Logout')
        logout_button.grid(column=0,row=3, sticky='e')
        logout_button.bind("<Button-1>",self.logout)
        logout_button.bind("<Return>",self.logout)


#------------------------------------------------------------------------------
#   It disconnects to server and returns to login tab
#------------------------------------------------------------------------------
    
    def logout(self,event):
        self.tab_controller.hide(self.contacts) 
        self.login_tab()


#------------------------------------------------------------------------------
#   It connects to server (search) for adding new contacts
#------------------------------------------------------------------------------

    def contacts_search(self,event):
        'Gets the text from the search field onthe login tab'
        'Calls the connect_remote server method'
        #'Returns the result'
        results ={}
        user = self.search_entry.get()
        #self.chat_button_user = user
        if user == '':
            self.search_message.set('Please enter a valid name')
        elif user == self.username:
            self.search_message.set('Cannot add yourself as a contact')
        else:
            self.options['search']['USER'] = user            
            results = (self.connect_remote_server(self.options['search']))
            
            if results['USER']!= '':
                'Pop up window to notify the user'
                if self.add_contact(results):
                    self.search_message.set('Contact added')
                    'The user is added to the local dictionary'
                    #self.contacts_dict['USER'] = user
                    'Display new contact'
                    'Add new contact to contacts_dict'
                    self.contacts_dict[results['USER']] = {}
                    self.display_contacts()

                else:                
                    self.search_message.set('Contact already added')
            else:
                self.search_message.set('User does not exist')

            self.search_entry.delete(0,END)


#------------------------------------------------------------------------------
#   It connects to server (add)
#------------------------------------------------------------------------------
    
    def add_contact(self, results):
        'Add a new contact to local database'
        print "try insert"
        self.options['add']['USER'] = self.username
        self.options['add']['CONTACT'] = results['USER']
        results = self.connect_remote_server(self.options['add'])
        return results


#------------------------------------------------------------------------------
#   It connects to server and get contacts list
#------------------------------------------------------------------------------

    def get_contacts(self):
        'Get contact list from the chatserver db'
        self.options['get']['USER'] = self.username
        results = self.connect_remote_server(self.options['get'])
        for each_contact in results:
            self.contacts_dict[each_contact] = {}


#------------------------------------------------------------------------------
#   It displays contacts as buttons to start chats
#------------------------------------------------------------------------------

    def display_contacts(self):
        'empty the display and fill it again'
        for child in self.contacts_listbox.interior.winfo_children():
            child.destroy()
        'Create one button for each contact'
        for username in sorted(self.contacts_dict.keys()):
            btn = Button(self.contacts_listbox.interior, width=20, #relief=FLAT, 
                #bg="gray99", fg="purple3",font="Dosis",
                text= username,
                command=lambda name=username:self.chat_button_clicked(name))
            #btn.bind("<Button-1>",self.chat_button_clicked)
            #btn.bind("<Return>",self.chat_button_clicked)
            btn.pack(padx=10, pady=5, side=TOP)
        

#------------------------------------------------------------------------------
#   It tries to connect to the contact and eventually opens the chat tab
#------------------------------------------------------------------------------
 
    def chat_button_clicked(self,name):  
        'Open a new chat tab if the contact is online'

        'try to connect:'
        'if connection is possible, open chat tab'
        'else communicate user offline'

        #self.chat_tab(self.chat_button_user)
        
        #if self.chat_connection(name):
        self.open_chat_tabs[name] = name
        self.chat_tab(name)
        #else:
        #    self.search_message.set(name+' is offline.')
        
        'set the focus on the new tab'#-----------------------------------------
        print 'open_chat_tabs + keys + name'
        print self.open_chat_tabs
        print self.open_chat_tabs.keys()
        print name


#------------------------------------------------------------------------------
#   It eventually connects to the server for starting a connection towards the contact
#------------------------------------------------------------------------------

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
                return True
                
            else:
                print('User is not online')
                return False
                ####Put a pop up window here
                #update client sock list after connect
    

#------------------------------------------------------------------------------
#   It starts the connection to the client
#------------------------------------------------------------------------------

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


#------------------------------------------------------------------------------
#   It opens the chat tab
#------------------------------------------------------------------------------
    
    def chat_tab(self,name):
        'This method has the controls and calls the methods for the chat window'        
        tab_name = Frame(self.tab_controller,name=name)        
        self.tab_controller.add(tab_name, text= name)
        'uncomment if tab needs to be active when msg received'
        #self.tab_controller.select(tab_name) take out bottom too
        self.tab_name_user[tab_name] = name
        conversation_frame = LabelFrame(tab_name, text=' Conversation ')
        conversation_frame.grid(column=0, row=0, padx=8, pady=4)
        
        display = Text(conversation_frame, bg="white", width=55, height=30, name='display') #witdh= number of characters that can be typed
        display.grid(column=0, row=1, sticky='W')
        self.user_tabs_list[name] = display

        'set focus'#---------------------------------------------------------
        self.user_tabs_list[name].focus_set()

        'Box to type message'
        submit_text = Entry(conversation_frame, width=35)
        submit_text.grid(column=0, row=2, padx=10, pady=5, ipady=5,sticky=W)
        submit_text.focus_set()
        'Send Button'
        send = Button(conversation_frame, text="Send")
        send.grid(column=0, row=2, padx=10,ipady=4, sticky=E)
        #check here - take out
        self.user_send_list[name] = submit_text #-----------------------------------
        print 'chat tab: user_send_list' #--------------------------------
        print self.user_send_list[name] #-------------------------------
        send.bind("<Button-1>",self.chat_send_button)
        send.bind("<Return>",self.chat_send_button)
        

#------------------------------------------------------------------------------
#   It starts the process for sending a message
#------------------------------------------------------------------------------

    def chat_send_button(self,event):
        'Gets the tab id, then calls the get_text method to update window'
        tab = self.tab_controller.select()
        print 'tab'
        print str(tab)        
        for key in self.tab_name_user.keys():
            print 'key'
            print str(key)           
            if str(tab) == str(key): #----------------
                user = (self.tab_name_user.get(key))
                print 'user'
                print user
            else: #------------------------------------
                print 'bohhhhhhhhhhhhhhh' #----------------------
        self.get_text(user)


#------------------------------------------------------------------------------
# It adds the message to the outgoing messages queue  
#------------------------------------------------------------------------------    

    def get_text(self,user):
        'Check if submit_text not empty and return data'
        message =''
        sent_data = {}
        if self.user_send_list[user].get() != '':
            message = self.user_send_list[user].get()
            self.update_window(user,message,True)
            #self.update_window(self.username,message)
            self.user_send_list[user].delete(0,END)
            sent_data['USER']= user
            sent_data['MSG'] = message
            
            'Add message to the outgoing queue'
            self.sent_messages.put_nowait(sent_data)
        
                  
#------------------------------------------------------------------------------
# not used
#------------------------------------------------------------------------------

    def mouse_enter(self,event):
        'Used by the send button to respond to mouse and enter key events'
        self.get_text()




#------------------------------------------------------------------------------
# It displays new text during the conversation   
#------------------------------------------------------------------------------

    def update_window(self,contact,message, is_myself):
        'Add text to the display when enter or send is pressed'
        print 'inside update_window'
        print self.user_tabs_list.keys()
        print contact

        self.user_tabs_list[contact].configure(state='normal') 
        if is_myself:               
            self.user_tabs_list[contact].insert(END,'{}: {}\n \n'.format(self.username,message))
        else:
            self.user_tabs_list[contact].insert(END,'{}: {}\n \n'.format(contact,message))
        self.user_tabs_list[contact].configure(state='disabled')
        
        

#------------------------------------------------------------------------------
#   It updates the chat window
#------------------------------------------------------------------------------              

    def gui_update(self):
        'Method called every second to update the window'
        #Might need to split the two trys in two methods'
        
        'Check the received_messages queue'        
        try:            
            received_message = self.received_messages.get_nowait()
            user = received_message['USER']
            msg = received_message['MSG']            
            print 'user'
            print user
            print 'in try - gui_update'

            'Check if tab exists for user or not'
            'Create new tab or update existing tab'
            self.user_tabs_list
            if user not in self.user_tabs_list.keys():                    
                self.chat_tab(user)
                print user
                print msg
                self.update_window(user,msg,False)
                print self.user_tabs_list
                print 'empty?'
            else:
                self.update_window(user,msg,False)
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
                    print sent_message
                    connected_client = self.user_connection.get(key)                                
                    print connected_client                    
                    'encode the message as json and send'
                    self.send_message(sent_message, connected_client)                                                  
        except:
            'Its ok if theres no data in the queue'
            'Will check again later'
            pass
        
        'Schedule gui_update again in one second'        
        self.demoPanel.after(1000, self.gui_update)



    

#------------------------------------------------------------------------------
#   It connects to the server 
#------------------------------------------------------------------------------

    def connect_remote_server(self,data):
        'Login Method'
        HOST = '127.0.0.1'
        PORT = 5001             
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        print data
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


#------------------------------------------------------------------------------
#   It connects to the contact client
#------------------------------------------------------------------------------
    #Use inheritance from the method above
    def connect_remote_client(self, host, port):
        'Method to connect to other clients'
        #data ={'USER': self.username, 'MSG':'Started a chat...'}
                     
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        print s
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


#------------------------------------------------------------------------------
#   It sends data to the connected client
#------------------------------------------------------------------------------

    def remote_client_send(self,sock):
        'Method to send data to the connected client'
        data ={'USER': self.username, 'MSG':'Started a chat...'}
        sock.send(data)
        print 'remote client recv thread started'
        while True:
            try:            
                sent_message = self.sent_messages.get_nowait()
                sent_message = json.dumps(sent_message).encode('utf-8')         
                sock.send(sent_message)
            except:
                pass
            

#------------------------------------------------------------------------------
#   It receives data to the connected client
#------------------------------------------------------------------------------

    def remote_client_recv(self,connected_client):
        'Method to receive data from connected client'
        size = 1024
        print 'remote client recv thread started'
        while True:
            received_data = connected_client.recv(size)
            if received_data:
                received_data = json.loads(received_data.decode('utf-8'))
                user = received_data['USER']
                self.user_connection[user] = connected_client
                self.received_messages.put_nowait(received_data)


#------------------------------------------------------------------------------
#   It initialises the local server
#------------------------------------------------------------------------------

    def local_server(self):
        'Initialise the instance with an IP address and port number'
        self.host = '127.0.0.1'#host
        self.port = 8080#port        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Create TCP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))  #Bind the socket (sock) to the host and port
    
        'Listens for connections from clients and spawns a new thread'
        try:
            print 'Server listening on {}:{}'.format(self.host,self.port)
            self.sock.listen(10)
        except:
            print 'Server not listening'
            #Need to put a break here
            
        while True:
            connected_client, client_address = self.sock.accept()
            #Need to log the IP address of the client (connection) at this stage
            #create a method to do it
            'Connection Times out after 60 secs'
            #connected_client.settimeout(120)   
            'Call thread with the client_handler method'
            thread.start_new_thread(self.client_handler,(connected_client, client_address))
            print '{}'.format(client_address)
            print '{}'.format(connected_client)


#------------------------------------------------------------------------------
#   It sends and receives data to/from the connected clients ----------------------------
#------------------------------------------------------------------------------

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
            print 'Client Handler thread started...'
        connected_client.close()


#------------------------------------------------------------------------------
# It sends data to connected clients  
#------------------------------------------------------------------------------

    def send_message(self,sent_message, connected_client):
        'Method to send data to the connected clients'
        'First encode as json and then send'
        result= json.dumps(sent_message).encode('utf-8')        
        try:            
            #####Something here?
            connected_client.sendall(result)
            print 'wednesday'
        except:
            print 'unable to send the message: '.format(message)

'''
#------------------------------------------------------------------------------
#  not used 
#------------------------------------------------------------------------------
    def client_handler2(self,connected_client, client_address):
        'Method to send data to the connected client'
        sent_message ={'USER': self.username, 'MSG':'Started a chat...'}
        sent_message = json.dumps(sent_message).encode('utf-8')
        size = 1024
        result = ''
        ip,host = client_address   
        connected_client.send(sent_message)
        print 'Client Handler 2 thread started...'
        while True:
            try:            
                sent_message = self.sent_messages.get_nowait()
                sent_message = json.dumps(sent_message).encode('utf-8')         
                connected_client.send(sent_message)                
            except:
                pass '''

    


#------------------------------------------------------------------------------
# Class for scrollable frame - buttons in contacts_tab 
# @author: http://stackoverflow.com/questions/31762698/dynamic-button-with-scrollbar-in-tkinter-python
#------------------------------------------------------------------------------

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw) 

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)



def create_db():
    'Create database to be used by client'
    con = sqlite3.connect('client.db')
    cur = con.cursor()
    cur.execute(""" CREATE TABLE contacts (username string primary key, date text)""")
    con.commit()
    con.close()  
    
def delete_db():
    'Delete client database'
    con = sqlite3.connect('client.db')
    cur = con.cursor()
    cur.execute(""" DROP TABLE """)
    con.commit()
    con.close()        
        
        

def run():
        
    chat = Client()
    'Start mainloop'
    chat.master.mainloop()   
    #chat.window.mainloop()   
 
           
                       

if __name__ == "__main__":
    run()
    #create_db()
    