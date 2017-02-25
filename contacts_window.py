# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 21:05:28 2017

@author: http://stackoverflow.com/questions/31762698/dynamic-button-with-scrollbar-in-tkinter-python
"""

from Tkinter import *


class User:
    def __init__(self, username):
        self.username = username
        self.is_online = True
        

'''s = User("Shweta")            
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
users_list.append(d)'''  




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

        '''def configure_scroll(self):


  #  scframe = VerticalScrolledFrame(root)
   # scframe.pack()

    #lis = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            #s = "Shweta"            
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
            for i, x in enumerate(users_list):
                btn = Button(self.interior, height=1, width=20, relief=FLAT, 
                    bg="gray99", fg="purple3",
                    font="Dosis", text='Button ' + users_list[i].username,
                    command=lambda i=i,x=x: openlink(i))
                btn.pack(padx=10, pady=5, side=TOP)

        def openlink(i):
            print users_list[i].username
    # open new window with chat
root = Tk()
root.title("Scrollable Frame Demo")
root.configure(background="gray99")
scframe = VerticalScrolledFrame(root,parent)
scframe.pack()
scframe.configure_scroll()
root.mainloop()'''