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
    list_of_tabs = {}
    tab_name_user = {}
    received_messages = queue.Queue()     
    sent_messages = queue.Queue()
    name = ['mary','john','joe']

    options = {'login': {'OPTION':'LOGIN','USER':username,'PASSWORD':password},
               'query': {'OPTION': 'QUERY_USER','USER':username},
               'update': {'OPTION': 'UPDATE_USER','USER':username},
               'new' : {'OPTION':'NEW_USER','USER': username,'PASSWORD': password}
               }


    def __init__(self):
        'This method initialises the basic window'
        self.received_messages = queue.Queue()
        self.sent_messages = queue.Queue()
        self.window = Tk()
        self.window.title("Synomilia Chat")
        thread.start_new_thread(self.local_server,())
        self.tab_controller = ttk.Notebook(self.window)
        #self.main = ttk.Frame(self.tab_controller)
        self.login_tab()
        self.main_tab()
        self.window.after(5000, func=self.gui_update)
        'Window main loop'
        self.window.mainloop()

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
        
        

    def chat_tab(self,tab_name,name):
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
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username != '' and password != '':
            self.options['login']['USER'] = username
            self.options['login']['PASSWORD'] = password
            if self.connect_remote_server(self.options['login']):             
                self.tab_controller.hide(self.login)
            else:
                print('Log in failed')
            
            
                #else:
                #self.username_entry.delete(0,END)
                #self.password_entry.delete(0,END)
            #sent_data['USER']= self.username
            #sent_data['MSG'] = message

    def gui_update(self):
        'Method called every second to update the window'
        'Check if message not empty'
        'Check if tab exists for user or not'
        'Create new tab or update existing tab'
        display_message = {}        
                
        while True:            
            if not self.received_messages.empty():
                
                received_message = self.received_messages.get_nowait()
                user = received_message['USER']
                msg = received_message['MSG']
                
                if user not in self.list_of_tabs.keys():                    
                    self.chat_tab(user,user)
                    self.update_window(user,msg)
                    print(self.list_of_tabs)
                else:
                    self.update_window(user,msg)
            else:
                return

    


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


    
        
        

def run():
        
    chat = Client()
    
   
    
    'If user details correct start local server to listen'
    '''if chat.connect_remote_server('marc','password'):
        thread.start_new_thread(chat.local_server,())
    while True:
        if not chat.received_messages.empty():
            pass
            #chat.chat_window()'''
           
                       

if __name__ == "__main__":
    run()
    
