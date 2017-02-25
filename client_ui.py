#!/usr/bin/env python


from Tkinter import *  # python3
from scroll2 import VerticalScrolledFrame    # python
from chat_window import *
from queue import Queue

TITLE_FONT = ("Helvetica", 18, "bold")

class ChatApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (StartPage,PageOne):
            page_name = F.__name__
            #print page_name
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        #label = Label(self, text="This is the start page", font=TITLE_FONT)
        #label.pack(side="top", fill="x", pady=10)
        #window.title("Synomilia Chat")

        label_inst = Label(self, text = "Please login to continue", 
                        fg = "#383a39", bg = "#a1dbcd")
        label_inst.pack()

        label_username = Label(self, text = "Username", fg = "#383a39", bg = "#a1dbcd")
        entry_username = Entry(self)

        label_username.pack()
        entry_username.pack()

        label_password = Label(self, text = "Password", fg = "#383a39", bg = "#a1dbcd")
        entry_password = Entry(self)

        label_password.pack()
        entry_password.pack()

        login_button = Button(self, text= "Login", fg = "#383a39", bg = "#a1dbcd",
                                    command=lambda: controller.show_frame("PageOne"))
        login_button.pack()



class PageOne(VerticalScrolledFrame):

    def __init__(self, parent, controller):
        VerticalScrolledFrame.__init__(self, parent)
        #scframe = VerticalScrolledFrame(self, parent)
        #scframe.pack()

        #lis = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        for i, x in enumerate(users_list):
            btn = Button(self.interior, height=1, width=20, relief=FLAT, 
                bg="gray99", fg="purple3",font="Dosis", text='Button ' + users_list[i].username,
                command=lambda i=i,x=x: self.create_chat_window(i))
            btn.pack(padx=10, pady=5, side=TOP)
        
        button = Button(self, text="Log Out",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def create_chat_window(self,i):
        #print users_list[i].username
        #s = User("Shweta")  
        #my_app = SingleChat(root, s)   
        win = Toplevel()
        win.title("Synomilia Chat ")
        sc = SingleChat(win, i)
        win.mainloop()

class User:
    def __init__(self, username):
        self.username = username
        self.is_online = True

s = User("Shweta")  
c = User("Checca")
a = User("Alice")            
b = User("Bob")
ch = User("Charlie")            
d = User("Diana")
            
users_list = []
users_list.append(c)
users_list.append(s)  
users_list.append(a)
users_list.append(b)  
users_list.append(ch)
users_list.append(d)  


if __name__ == "__main__":
    app = ChatApp()
    app.wm_geometry("250x250")
    app.mainloop()
              


