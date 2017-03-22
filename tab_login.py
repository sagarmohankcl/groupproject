import socket
import json
import threading
import thread
import Queue as queue
from Tkinter import *
#import tkinter as tk
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
    l =[]    
    user_tabs_list = {}
    user_send_list = {}
    list_of_tabs = {}
    tab_name_user = {}
    received_messages = queue.Queue()     
    sent_messages = queue.Queue()
    name = ['mary','john','joe']
    chat_button_user =''

    options = {'login': {'OPTION':'LOGIN','USER':username,'PASSWORD':password},
               'query': {'OPTION': 'QUERY_USER','USER':username},
               'update': {'OPTION': 'UPDATE_USER','USER':username},
               'new' : {'OPTION':'NEW_USER','USER': username,'PASSWORD': password},
               'search': {'OPTION': 'SEARCH_USER', 'USER':username}
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

        #--- create description tab
        #--- frame to hold (tab) content
        self.login_tab() 
        #self.received_messages = queue.Queue()
        #self.sent_messages = queue.Queue()
        #self.window = Tk()
        #self.window.title("Synomilia Chat")
        #thread.start_new_thread(self.local_server,())
        #self.tab_controller = ttk.Notebook(self.window)#,width=500, height=550)
        
        #self.login_tab()
        #self.main_tab()
        #'Schedule gui_update to run on the main thread in one second'
        #self.window.after(1000, self.gui_update)'''
        
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


        
    #def logout(self):

    def chat_tab(self,name):
        'This method has the controls and calls the methods for the chat window'        
        tab_name = Frame(self.tab_controller,name=name)        
        self.tab_controller.add(tab_name, text= name)
        'uncomment if tab needs to be active when msg received'
        #self.tab_controller.select(tab_name) take out bottom too
        self.tab_name_user[tab_name] = name
        conversation_frame = LabelFrame(tab_name, text=' Conversation ')
        conversation_frame.grid(column=0, row=0, padx=8, pady=4)
        
        display = Text(conversation_frame, bg="white", width=60, height=30, name='display')
        display.grid(column=0, row=1, sticky='W')
        self.user_tabs_list[name] = display
        
        'Box to type message'
        submit_text = Entry(conversation_frame, width=60)
        submit_text.grid(column=0, row=2, padx=3, pady=5, ipady=5,sticky=W)
        'Send Button'
        send = Button(conversation_frame, text="Send")
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
        contacts_listbox = Treeview(listbox_frame)
        contacts_listbox.grid(column=0,row=1, pady=4, ipadx=2, ipady=2, sticky='w')
        
        'Add Search'
        self.search_entry = Entry(listbox_frame)
        self.search_entry.grid(column=0, row=2, padx=1, pady=3,sticky='w')
        search_button = Button(listbox_frame, text='Add Contact')
        search_button.grid(column=0,row=2, sticky='e')
        search_button.bind("<Button-1>",self.contacts_search)
        search_button.bind("<Return>",self.contacts_search)

        'Add Logout Button'
        logout_frame = Frame(self.contacts,width=180, height=180)
        logout_frame.grid(column=0, row=2)#,padx=4, pady=4, columnspan=2)#, sticky='newss')
        logout_button = Button(logout_frame, text='Logout')
        logout_button.grid(column=0,row=3, sticky='e')
        logout_button.bind("<Button-1>",self.logout)
        logout_button.bind("<Return>",self.logout)




    def contacts_search(self,event):
        'Gets the text from the search field onthe login tab'
        'Calls the connect_remote server method'
        'Returns the result'
        results ={}
        user = self.search_entry.get()
        self.chat_button_user = user
        if user != '':
            self.options['search']['USER'] = user            
            results = (self.connect_remote_server(self.options['search']))
            
            if results['USER']!= '':
                'Pop up window to notify the user'
                #notify = Toplevel()
                #notify.title('Search User')
                #msg = Message(notify, text='User found',width=80)
                #msg.pack()
                #login_frame = Frame(notify)
                #login_frame.pack()
                #chat_button = Button(login_frame, text='Message User',width=15)
                #chat_button.pack()
                #chat_button.bind("<Button-1>",self.chat_button_clicked)
                #contacts_add = Button(login_frame, text='Add Contact',width=15)
                #contacts_add.pack()
                result = self.add_contact(results)
                
                
            else:                
                'Pop up window to notify the user'
                notify = Toplevel()
                notify.title('Search User')
                msg = Label(notify, text='User not found')
                msg.pack()
            self.search_entry.delete(0,END)

    def chat_button_clicked(self,event):
        'Open a new chat tab'
        self.chat_tab(self.chat_button_user)
        
    def add_contact(self, results):
        'Add a new contact to local contact list'
        print "try insert"
        try: 
            con = sqlite3.connect('client.db')
            cur = con.cursor()  
            cur.execute("INSERT INTO contacts VALUES (?,?)", (results['USER'].lower(), results['DATE'].lower()))
            con.commit() 
            print "inserted"     
        except:
            return False
        con.close()
        return True


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
        #login_icon = PhotoImage(file='chaticon.png')
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
        self.username_entry.grid(column=2, row=1, pady=3,sticky=E)

        self.password_entry = Entry(self.credential_frame, show="*")
        self.password_entry.grid(column=2, row=2, pady=3,sticky=E)

        #newuser_label = ttk.Label(credential_frame, text='New User:')
        #newuser_label.grid(column=1, row=4, sticky='w')
        #newuser_checkbutton = ttk.Checkbutton(credential_frame,
        #                                     variable=newuser_var,
        #                                      offvalue=0,
        #                                      onvalue=1)
        
        #newuser_checkbutton.grid(column=2, row=4, sticky='w')
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



    def login_submit(self,event):
        'Gets the text from the username and password field on the login tab'
        'Calls the connect_remote server method'
        'Hides the login tab'
        'Calls the Main tab'
        username = self.username_entry.get()
        password = self.password_entry.get()        
        if username != '' and password != '':
            self.options['login']['USER'] = username
            self.options['login']['PASSWORD'] = encrypt(password)
            if self.connect_remote_server(self.options['login']):             
                self.contacts_tab()
                self.tab_controller.hide(self.login)                
            else:
                #alert_label = ttk.Label(self.credential_frame, text='Username or password mismatching')
                #alert_label.grid(columnspan=3)
                self.alert_message.set('Username or password mismatching')
                #self.username_entry.delete(0,END)
                #self.password_entry.delete(0,END)
                #'Pop up window to notify the user'   # make a label?-----------------
                #notify = Toplevel()
                #notify.title('Failed Login')
                #msg = Message(notify, text='Login Failed')
                #msg.pack()
        else:
            self.alert_message.set('Username or password missing')
            #alert_label = ttk.Label(self.credential_frame, text='Username or password missing')
            #alert_label.grid(columnspan=3)

    
    def logout(self,event):
        self.tab_controller.hide(self.contacts) 
        self.login_tab()




    
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

    def register_submit(self,event):
        'Gets the text from the username and password field on the login tab'
        'Calls the connect_remote server method'
        'Close registration window'
        #'Hides the login tab'
        'Calls the Main tab'
        username = self.username_entry.get()
        password_1 = self.password_entry_1.get() 
        password_2 = self.password_entry_2.get() 

        if username != '' and password_1 != '' and (password_1 == password_2):
            self.options['new']['USER'] = username
            self.options['new']['PASSWORD'] = encrypt(password_1)
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
                
                

    def gui_update(self):
        'Method called every second to update the window'        
                
        try:            
            received_message = self.received_messages.get_nowait()
            user = received_message['USER']
            msg = received_message['MSG']

            'Check if tab exists for user or not'
            'Create new tab or update existing tab'  
            if user not in self.list_of_tabs.keys():                    
                self.chat_tab(user)
                self.update_window(user,msg)
                print(self.list_of_tabs)
            else:
                self.update_window(user,msg)
        except: #QueueEmpty: Need to find the exception to catch it here
            'Its ok if theres no data in the queue'
            'Will check again later'
            pass
        'Schedule gui_update again in one second'
        self.window.after(1000, self.gui_update)

    


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
            connected_client.settimeout(120)   
            'Call thread with the client_handler method'
            thread.start_new_thread(self.client_handler,(connected_client, client_address))
            print('{}'.format(client_address))
            print('{}'.format(connected_client))


    def client_handler(self,connected_client, client_address):
        'Send and receive data from each client that connects'        

        size = 1024
        result = ''
        while True:
            received_data = connected_client.recv(size)
            received_data = json.loads(received_data.decode('utf-8'))            
            ip,host = client_address            
            if received_data:                
                self.received_messages.put_nowait(received_data)
                print(received_data)
                print(self.received_messages)
                l= received_data
            'if not self.sent_messages.empty():'
            'when the connection is accepted do a list of IPs, then check'
            'then check that list when sending'
            'Need to check who the message has to go to'
            'encode and send'
                
            

            result = json.dumps(result).encode('utf-8')                
            connected_client.send(result)
            
            
    def receive(self):
        'Method to receive data from to remote client'
        while True:
            if not self.received_messages.empty():
                print(self.received_messages.get_nowait())
        


    def send_message(self,message):
        'Method to send data to the sent_messages queue'
        self.sent_messages.put_nowait(message)
        
    
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
            #self.send_message(sent_data)
            #Add message directly to the queue instead
            self.sent_messages.put_nowait(message)
        
            
        

    def mouse_enter(self,event):
        'Used by the send button to respond to mouse and enter key events'
        self.get_text()




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
    
