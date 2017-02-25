# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 12:37:29 2017

@author: Checca
"""

from Tkinter import *
from queue import Queue


class SingleChat:
    def __init__(self, my_parent, user): 
        self.parent = my_parent
        self.in_msg = "not yet integrated"
        self.out_msg = ""
        
        self.in_queue = Queue()
        self.out_queue = Queue()
        
        self.in_queue.enqueue("Hi-1") #----------- to delete
        self.in_queue.enqueue("Hi-2")
        self.in_queue.enqueue("Hi-3")
                
        self.my_container1 = Frame(my_parent)
        self.my_container1.pack()
        
        self.text = Text(self.my_container1)
        self.text.pack()
        
        self.button1 = Button(self.my_container1, command = self.print_out_msg, text = "Enter", background = "grey")
        self.button1.pack(side = RIGHT)
        self.button1.focus_force() # it's focused when the program starts
        
        self.entry = Entry(self.my_container1, width = 50)
        self.entry.pack()
        self.entry.insert(0,"type your message")
        
   
        
        
    def print_out_msg(self):
        self.out_queue.enqueue(self.entry.get())
        #self.out_msg = "Me: " + self.out_queue.dequeue() + "\n"
        self.entry.delete(0,END)
        self.text.insert(END, "Me: " + self.out_queue.dequeue() + "\n") #--------------to modify
        #self.text.insert(END, user.username + " " + self.in_queue.dequeue() + "\n")#---------to modify
    
  #  def print_in_msg(self, in_msg):
      #  self.in_queue.enqueue("not yet integrated")
       # self.in_msg = user.username + " " + self.in_queue.dequeue() + "\n"
        
    def fake_conversation(self):  
        self.in_queue.enqueue("Hi-1")
        self.in_queue.enqueue("Hi-2")
        self.in_queue.enqueue("Hi-3")
        
    
    def conversation(self):
        while self.in_queue or self.out_queue:
            self.text.insert(END, "Me: " + self.out_queue.dequeue() + "\n")
            #self.text.insert(END, user.username + " " + self.in_queue.dequeue() + "\n") 
        
"""
class User:
    def __init__(self, username):
        self.username = username
        self.is_online = True
        

s = User("Shweta")              
            
root = Tk()
root.title("Synomilia Chat")
my_app = SingleChat(root, s)                     
#my_app.fake_conversation()
print my_app.in_queue
my_app.conversation
root.mainloop()
"""