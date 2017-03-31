import socket
import json
import threading
import thread
import Queue as queue
from Tkinter import *
#import tkinter as tk  fpr python 3 
#from tkinter 
from ttk import *
import tkMessageBox as messagebox
from PIL import Image, ImageTk
import time
import encrypt_password
from encrypt_password import *
import sqlite3
import os.path
from external_sources import *

#------------------------------------------------------------------------------
#   Chat appliccation client
#------------------------------------------------------------------------------

class Client(object):
    username = ''
    password =''
    connection = ''
    client_port = 8080
    user = ''
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
    contacts_dict = {} 

    request = {'login': {'OPTION':'LOGIN','USER':username,'PASSWORD':password},
               'query': {'OPTION': 'QUERY_USER','USER':username},
               'update': {'OPTION': 'UPDATE_USER','USER':username},
               'new' : {'OPTION':'NEW_USER','USER': username,'PASSWORD': password},
               'search': {'OPTION': 'SEARCH_USER', 'USER':username},
               'add' : {'OPTION': 'ADD_USER', 'USER':username, 'CONTACT': ''},
               'get': {'OPTION': 'GET_CONTACTS', 'USER':username}
               }
    
#------------------------------------------------------------------------------
#   Initialises the basic window
#------------------------------------------------------------------------------

    def __init__(self):
        self.master = Frame(name='general')
        self.root = self.master.master  # short-cut to top-level window
        self.master.pack()  # pack the Frame into root, defaults to side=TOP
        self.root.title('Synomilia Chat')  # name the window
        #self.root.protocol("WM_DELETE_WINDOW", self.closing)
        
        
        self.demoPanel = Frame(self.master, name='demo')  # create a new frame slaved to master
        self.demoPanel.pack()  # pack the Frame into root

        # create (notebook) demo panel
        self.tab_controller = Notebook(self.demoPanel, name='notebook',width=400, height=550)  # create the ttk.Notebook widget
        #self.tab_controller = CustomNotebook(self.demoPanel, name='notebook',width=420, height=550)  # create the ttk.Notebook widget
        self.tab_controller.grid_propagate(True)
        
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
#   Displays the login page
#------------------------------------------------------------------------------

    def login_tab(self):
        self.login = Frame(self.tab_controller, name='login')
        self.tab_controller.add(self.login, text= 'Login')
        
        'Add Icon'
        login_icon_frame = Frame(self.login)
        login_icon_frame.pack(side='top',expand=1) #without expand, the icon stays fix while registration
        login_icon = ImageTk.PhotoImage(Image.open('chat-2-icon.png'))
        login_icon_label = Label(login_icon_frame, image=login_icon)
        login_icon_label.image = login_icon
        login_icon_label.pack(fill='both')
        
        'Add labels and buttons'
        self.credential_frame = LabelFrame(self.login, text='Login')#, height=50, width=100)
        self.credential_frame.pack(expand=1,side='top')

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
        submit_button.bind("<ButtonRelease-1>",self.login_submit)

        submit_button.bind("<Return>",self.login_submit)

        register_button = Button(self.credential_frame, text='Register')
        register_button.grid(column=1,row=4, columnspan=2, sticky='w')
        register_button.bind("<ButtonRelease-1>",self.register_newuser)
        register_button.bind("<Return>",self.register_newuser)

        self.alert_message = StringVar()
        self.alert_label = Label(self.credential_frame, textvariable=self.alert_message, foreground='red')
        self.alert_label.grid(columnspan=3)

#--------------------------------------------------------------------------------------
#   Connects to the remote chatserver and displays the current contact list of the user
#--------------------------------------------------------------------------------------

    def login_submit(self,event):
        'Gets the text from the username and password field on the login tab'
        'Calls the connect_remote server method'
        'Hides the login tab'
        'Calls the Main tab'
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()        
        if self.username != '' and self.password != '':
            self.request['login']['USER'] = self.username
            self.request['login']['PASSWORD'] = encrypt(self.password)
            if self.connect_remote_server(self.request['login']):  
                print self.username + " is online"           
                self.contacts_tab()
                self.tab_controller.hide(self.login) 
                              
            else:
                #print self.password
                self.alert_message.set('Username or password mismatching')
                self.root.after(2000,self.clean_label)
        else:
            self.alert_message.set('Username or password missing')
            self.root.after(2000,self.clean_label)

#------------------------------------------------------------------------------
#   Displays a pop up window for registering a new user
#------------------------------------------------------------------------------
    
    def register_newuser(self, event):
        'Open new window and allow registration of a new user'
        self.register_w = Toplevel()
        self.register_w.protocol("WM_DELETE_WINDOW", self.closing)

        self.credential_frame_R = LabelFrame(self.register_w, text='Registration new user')
        self.credential_frame_R.grid(column=0,row=1,padx=85, pady=4, ipadx=2, ipady=2, sticky='w')

        username_label = Label(self.credential_frame_R, text='Username: ')
        username_label.grid(column=1, row=1, sticky=W)
        self.username_entry = Entry(self.credential_frame_R)
        self.username_entry.grid(column=2, row=1, pady=3,sticky=E)
        self.username_entry.focus_set()

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
        
        self.credential_frame.pack_forget() # makes the credential frame disappear

#------------------------------------------------------------------------------
#   Closes registration window and returns to the login page
#------------------------------------------------------------------------------

    def closing(self):
            if messagebox.askokcancel("Quit", "Do you want to go back to the login page?"):
                self.register_w.destroy()
                #self.credential_frame.grid(column=0,row=1,padx=105, pady=4, ipadx=2, ipady=2, sticky='w')
                self.credential_frame.pack(expand=1,side='top')
            else:
                pass

#------------------------------------------------------------------------------
#   Connects to server and submits user's credentials for registration
#------------------------------------------------------------------------------

    def register_submit(self,event):
        'Gets the text from the username and password field on the login tab'
        'Calls the connect_remote server method'
        'Close registration window'
        'Hides the login tab'
        'Calls the Main tab'
        self.username = self.username_entry.get()
        password_1 = self.password_entry_1.get() 
        password_2 = self.password_entry_2.get() 

        if self.username != '' and password_1 != '' and (password_1 == password_2):
            self.password = password_1
            self.request['new']['USER'] = self.username
            self.request['new']['PASSWORD'] = encrypt(self.password)
            if self.connect_remote_server(self.request['new']):             
                self.contacts_tab()
                self.tab_controller.hide(self.login)
                self.register_w.destroy()    
                print self.username + " registered successfully"  
                print self.username + " is online"          
            else:
                self.username_entry.delete(0,END)
                self.password_entry_1.delete(0,END)
                'Pop up window to notify the user'   
                notify = Toplevel()
                notify.title('Failed Registration')
                msg = Message(notify, text='Registration Failed')
                msg.pack()
        else:
            alert_label = Label(self.credential_frame_R, text='Username missing or password mismatching', foreground='red')
            alert_label.grid(columnspan=3)

#------------------------------------------------------------------------------
#   Displays the chat app interface with the user's contact list
#------------------------------------------------------------------------------

    def contacts_tab(self):
        self.contacts = Frame(self.tab_controller, name='contacts')
        self.tab_controller.add(self.contacts, text='Contacts')
        
        'Adding app icon'
        contacts_icon_frame = Frame(self.contacts)
        contacts_icon_frame.pack(side='top')
        
        contacts_icon = ImageTk.PhotoImage(Image.open('chat-2-icon_small.png'),width=5,height=5)
        contacts_icon_label = Label(contacts_icon_frame, image=contacts_icon, width=5)
        contacts_icon_label.image = contacts_icon
        contacts_icon_label.pack(side='right', padx=5,pady=5)
        
        msg = 'Hello '+self.username+',\nthis is Synomilia Chat 1.0.\nEnjoy!'
        welcome_msg = Label(contacts_icon_frame,text=msg,foreground='blue',justify='center')
        welcome_msg.pack(side='left',fill='both',expand=1,padx=10)
        
        'Add listbox to the frame'
        listbox_frame = Frame(self.contacts)
        listbox_frame.pack(side='top')
        self.contacts_listbox = VerticalScrolledFrame(listbox_frame)
        
        'Get previously added contacts and display'
        has_contacts = self.get_contacts()
        if has_contacts:
            self.display_contacts()
        
        'Add Search'
        self.search_entry = Entry(listbox_frame)
        self.search_entry.grid(column=0, row=1, padx=1, pady=3,sticky='w')
        search_button = Button(listbox_frame, text='Add Contact')
        search_button.grid(column=1,row=1, sticky='e')
        search_button.bind("<Button-1>",self.contacts_search)
        search_button.bind("<Return>",self.contacts_search)

        'Label for communication about response'
        self.search_label = Label(listbox_frame, textvariable=self.alert_message, foreground='blue')
        self.search_label.grid(row=2,columnspan=3)

        'Add Logout Button'
        logout_frame = Frame(self.contacts)
        logout_frame.pack(side='top')
        logout_button = Button(logout_frame, text='Logout')
        logout_button.pack()
        logout_button.bind("<ButtonRelease-1>",self.logout)
        logout_button.bind("<Return>",self.logout)

#------------------------------------------------------------------------------
#   Disconnects the connection from server and returns to login page
#------------------------------------------------------------------------------
    
    def logout(self,event):
        if messagebox.askokcancel("Log Out", "Are you sure?"):
            self.tab_controller.hide(self.contacts)
            for tab in self.tab_name_user.keys():
                self.tab_controller.hide(tab) 
            self.login_tab()
        else:
            pass

#-----------------------------------------------------------------------------------------
#   Connects to the remote chatserver to search if the contact entered by the user exists
#-----------------------------------------------------------------------------------------

    def contacts_search(self, event):
        'Gets the text from the search field on the login tab'
        'Calls the connect_remote server method'
        'Calls the add_contact method'
        response ={}
        contact = self.search_entry.get()
        if contact == '':
            self.alert_message.set('Please enter a valid name')
            self.root.after(3000,self.clean_label)
        elif contact == self.username:
            self.alert_message.set('Cannot add yourself as a contact')
            self.root.after(3000,self.clean_label)
        else:
            self.request['search']['USER'] = contact  
            print "Searching for " + contact         
            response = (self.connect_remote_server(self.request['search']))
            if response['USER']!= '':
                print contact + " found"
                'Call the add_contact method with the received response'
                if self.add_contact(response):
                    'If add_contact returns true notify that the contact is added'
                    self.alert_message.set(contact + ' added')
                    self.root.after(3000,self.clean_label)
                    print contact + " added"

                    'The user is added to the local dictionary'
                    'Display new contact'
                    'Add new contact to contacts_dict'
                    self.contacts_dict[response['USER']] = {}
                    self.display_contacts()
                else:                
                    print contact + " already added"
                    self.alert_message.set(contact + ' already added')
                    self.root.after(3000,self.clean_label)
            else:
                print contact + " does not exist"
                self.alert_message.set(contact + ' does not exist')
                self.root.after(3000,self.clean_label)
            self.search_entry.delete(0,END)

#------------------------------------------------------------------------------
#   Cleans the content of the alert_label
#------------------------------------------------------------------------------

    def clean_label(self):
        self.alert_message.set('')

#------------------------------------------------------------------------------------------------
#   Connects to the remote chatserver for adding new contacts to the user's contact list
#------------------------------------------------------------------------------------------------
    
    def add_contact(self, response):
        print "Adding " + response['USER'] + "..."
        self.request['add']['USER'] = self.username
        self.request['add']['CONTACT'] = response['USER']
        response = self.connect_remote_server(self.request['add'])
        return response

#------------------------------------------------------------------------------
#   Connects to the remote chatserver and fetches user's contacts list
#------------------------------------------------------------------------------

    def get_contacts(self):
        print "Fetching contacts..."
        self.request['get']['USER'] = self.username
        response = self.connect_remote_server(self.request['get'])
        for each_contact in response:
            self.contacts_dict[each_contact] = {}
        if len(self.contacts_dict) > 0:
            return True
        else:
            return False

#------------------------------------------------------------------------------
#   Displays contacts as buttons that can be clicked to start chats
#------------------------------------------------------------------------------

    def display_contacts(self):
        'grid the scrollbar'
        self.contacts_listbox.grid(columnspan=2,row=0, pady=4, ipadx=2, ipady=2, sticky='nswe')
        'empty the display and fill it again'
        for child in self.contacts_listbox.interior.winfo_children():
            child.destroy()
        'Create one button for each contact'
        for username in sorted(self.contacts_dict.keys()):
            btn = Button(self.contacts_listbox.interior, width=20, text= username,
                command=lambda name=username:self.chat_button_clicked(name))
            btn.pack(padx=10, pady=5, side=TOP)
        

#------------------------------------------------------------------------------
#    Connect to the contact(remote client) and opens the chat tab
#------------------------------------------------------------------------------
 
    def chat_button_clicked(self,name):  
        'Open a new chat tab if the contact is online'
        'try to connect:'
        'if connection is possible, open chat tab'
        'else communicate user offline'
        if self.chat_connection(name):
            self.chat_tab(name)
        else:
            self.alert_message.set(name+' is offline.')
            self.root.after(3000,self.clean_label)
        'set the focus on the new tab'#-----------------------------------------
        print name


#-----------------------------------------------------------------------------------------
#   Connects to the chatserver for initiating a connection with the contact(remote client)
#-----------------------------------------------------------------------------------------

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
            self.request['query']['USER'] = name
            print "Querying the server for "+ name +"..."
            response = (self.connect_remote_server(self.request['query']))            
            if response['CONNECTION'] != '':
                host,port = response['CONNECTION'].split(':')
                'Connect to the remote client and get the socket information'
                'Store name and socket details in global list'
                print host
                print self.client_port
                connected_client = self.connector(host,self.client_port)
                self.user_connection[name] = connected_client
                return True  
            else:
                print('User is not online')
                return False
                ####Put a pop up window here
                #update client sock list after connect
    

#------------------------------------------------------------------------------
#   Initiates the connection to the contact(remote client)
#------------------------------------------------------------------------------

    def connector(self, host, port):
        'Method to initiate TCP connection to client'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msg = 'started a chat...'
        data = {'USER': self.username,'MSG':msg}        
        data = json.dumps(data).encode('utf-8')
        
        print host
        print port

        'Start the connection and send initial message'
        sock.connect((host, port))
        sock.send(data)
        'Start thread to receive messages'
        'Can take out host but need to modify the method below'
        thread.start_new_thread(self.client_handler,(sock, host))
        return sock


#------------------------------------------------------------------------------
#    Opens the chat tab for starting a conversation
#------------------------------------------------------------------------------
    
    def chat_tab(self,name):
        'This method has the controls and calls the methods for the chat window'        
        tab_name = Frame(self.tab_controller,name=name)        
        self.tab_controller.add(tab_name, text= name)
        'uncomment if tab needs to be active when msg received'
        #self.tab_controller.select(tab_name) take out bottom too
        self.tab_name_user[tab_name] = name
        exit_frame = Frame(tab_name)
        exit_frame.pack()
        
        info_msg = 'This is your conversation with '+name
        info = Label(exit_frame,text=info_msg)
        info.pack(side='left',fill='x',expand=1, ipadx=10,ipady=5)
        
        close_conversation = Button(exit_frame,text='Close',command=lambda name=tab_name:self.leave_conversation(name))
        close_conversation.pack(side='right')
        
        conversation_frame = LabelFrame(tab_name, text=' Conversation ')
        conversation_frame.pack(fill='both',expand=1)
        #conversation_frame.grid(column=0, row=1, padx=8, pady=4)
        display = Text(conversation_frame, wrap='word',bg="white", width=45, height=27, name='display', state='disabled') #witdh= number of characters that can be typed
        display.grid(column=0, row=0, sticky='nswe')
        self.user_tabs_list[name] = display
        scroll = Scrollbar(conversation_frame,command=display.yview)
        scroll.grid(column=1,row=0,sticky='ns')
        display.config(yscrollcommand= scroll.set)

        'Box to type message'
        submit_text = Entry(conversation_frame, width=40)
        submit_text.grid(column=0, row=1, padx=10, pady=5, ipady=5,sticky='sw')
        submit_text.focus_set()
        'Send Button'
        send = Button(conversation_frame, text="Send")
        send.grid(column=0, row=1, padx=10,ipady=5, sticky='se')
        #check here - take out
        self.user_send_list[name] = submit_text 
        #print self.user_send_list[name] 
        send.bind("<ButtonRelease-1>",self.chat_send_button)
        send.bind("<Return>",self.chat_send_button)
        return tab_name 

#------------------------------------------------------------------------------
#    Starts the process for sending a message to the remote client
#------------------------------------------------------------------------------

    def chat_send_button(self, event):
        'Gets the tab id, then calls the get_text method to update window'
        tab = self.tab_controller.select()
        print 'tab'
        #print str(tab)        
        for key in self.tab_name_user.keys():
            print 'key'
            print str(key)           
            if str(tab) == str(key): 
                self.user = (self.tab_name_user.get(key))
                print 'user'
                print self.user
            else: 
                print "hi"
        self.get_text(self.user)

#------------------------------------------------------------------------------
#   Adds the chat text message to the outgoing messages queue  
#------------------------------------------------------------------------------    

    def get_text(self, user):
        'Check if submit_text not empty and return data'
        message =''
        sent_data = {}
        if self.user_send_list[user].get() != '':
            message = self.user_send_list[user].get()
            self.update_window(user,message,True)
            #self.update_window(self.username,message)
            self.user_send_list[user].delete(0, END)
            sent_data['USER']= self.username
            sent_data['MSG'] = message
            print sent_data
            'Add message to the outgoing queue'
            self.sent_messages.put_nowait(sent_data)
 
#------------------------------------------------------------------------------
#   Closes the chat tab for the contact 'name'
#------------------------------------------------------------------------------

    def leave_conversation(self, name):
        if messagebox.askokcancel("Close", "Are you sure?"):
            self.tab_controller.hide(name)
            self.tab_controller.select(self.contacts)
         
#------------------------------------------------------------------------------
# not used
#------------------------------------------------------------------------------

    def mouse_enter(self,event):
        'Used by the send button to respond to mouse and enter key events'
        self.get_text()

#------------------------------------------------------------------------------
#   Displays new text messages during the conversation   
#------------------------------------------------------------------------------

    def update_window(self, contact, message, is_myself):
        'Add text to the display when enter or send is pressed'
        print 'inside update_window'
        #print self.user_tabs_list.keys()
        #print contact
        print "received message: "+ message

        self.user_tabs_list[contact].configure(state='normal') 
        if is_myself:
            self.user_tabs_list[contact].tag_config('me',foreground='blue')               
            self.user_tabs_list[contact].insert(END,'{}: {}\n \n'.format(self.username,message),'me')
        else:
            self.user_tabs_list[contact].tag_config('contact',foreground='black')    
            self.user_tabs_list[contact].insert(END,'{}: {}\n \n'.format(contact,message),'contact')
        self.user_tabs_list[contact].see(END)

        self.user_tabs_list[contact].configure(state='disabled')
        
#------------------------------------------------------------------------------
#   Updates the chat window every second
#------------------------------------------------------------------------------              

    def gui_update(self):
        #Might need to split the two trys in two methods'
        'Check the received_messages queue'        
        try:            
            received_message = self.received_messages.get_nowait()
            user = received_message['USER']
            msg = received_message['MSG']            
            print user + " started a chat"
            print "updating chat window"

            'Check if tab exists for user or not'
            'Create new tab or update existing tab'
            self.user_tabs_list
            if user not in self.user_tabs_list.keys():                    
                self.chat_tab(user)
                #print user
                #print msg
                self.update_window(user, msg, False)
                #print self.user_tabs_list
                #print self.open_chat_tabs
                #print 'empty?'
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
                if self.user == str(key):
                    'Get the connection string'
                    print "sent message " + sent_message
                    connected_client = self.user_connection.get(key)                                
                    #print connected_client                    
                    'encode the message as json and send'
                    self.send_message(sent_message, connected_client)                                                  
        except:
            'Its ok if theres no data in the queue'
            'Will check again later'
            pass
        'Schedule gui_update again in one second'        
        self.demoPanel.after(1000, self.gui_update)


#------------------------------------------------------------------------------
#   Connects to the remote chatserver
#------------------------------------------------------------------------------

    def connect_remote_server(self, data):
        'Login Method'
        #HOST = '10.40.212.51'
        HOST = ''
        PORT = 5001             
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        print 'Request payload: {}'.format(data)
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
#   Connects to the other clients
#------------------------------------------------------------------------------
    #Use inheritance from the method above
    def connect_remote_client(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        data = json.dumps(data).encode('utf-8')        
        s.connect((host, port))            
        

#------------------------------------------------------------------------------
#   Sends message to the connected client
#------------------------------------------------------------------------------

    def remote_client_send(self,sock):
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
#   Receives data from the connected client
#------------------------------------------------------------------------------

    def remote_client_recv(self,connected_client):
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
#   Localserver for listening from other clients
#------------------------------------------------------------------------------

    def local_server(self):
        'Initialise the instance with an IP address and port number'
        self.host = ''#host
        self.port = 8080#port        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Create TCP socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))  #Bind the socket (sock) to the host and port
        'Listens for connections from clients and spawns a new thread'
        try:
            print 'Client server listening on {}:{}'.format(self.host,self.port)
            self.sock.listen(10)
        except:
            print 'Client server not listening'
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
#   Sends and receives data to/from the connected clients 
#------------------------------------------------------------------------------

    def client_handler(self,connected_client, client_address):  
        size = 1024
        result = ''       
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
#   Sends json encoded chat message to connected clients  
#------------------------------------------------------------------------------

    def send_message(self, sent_message, connected_client):
        result = json.dumps(sent_message).encode('utf-8')        
        try:            
            connected_client.sendall(result)
            print 'Message sent'
        except:
            print 'Unable to send the message: '.format(message)


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
           
                     

if __name__ == "__main__":
    run()
    #create_db()
    
