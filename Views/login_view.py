from cProfile import label
from tkinter import *

class LoginView(Frame):
    def __init__(self,container:Misc):
        super().__init__(container)

        options = {'padx':5,'pady':5}


        #display frame
        self.pack(**options)

        self.password = StringVar()
        self.username = StringVar()
        self.password_info = StringVar()

        # define widgets
        self.label = Label(self, text='Login', font=('Arial', 40, 'bold'))
        self.lb_username = Label(self,text='Enter Username' , font=('Arial',10),padx=0,pady=0)
        self.entry_username = Entry(self, textvariable=self.username)
        self.lb_password = Label(self,text='Enter Password',font=('Arial',10))
        self.entry_password = Entry(self, show='*', textvariable=self.password)
        self.btn_login = Button(self,text='Login', command=self.login, state=ACTIVE)
        self.lb_password_info = Label(self, justify=LEFT, textvariable=self.password_info)

        # events
        self.entry_username.bind("<KeyRelease>", self.on_username_change_callback)
        self.entry_password.bind("<KeyRelease>", self.on_password_change_callback)

        self.label.grid(row=0, column=0,columnspan=2)
        self.lb_username.grid(row=1,column=0)
        self.entry_username.grid(row=1, column=1)
        self.lb_password.grid(row=2,column=0)
        self.entry_username.focus()
        self.entry_password.grid(row=2, column=1)
        self.btn_login.grid(row=4, column=0,columnspan=2)
        self.lb_password_info.grid(row=3, column=0,columnspan=2)
        # otan den 3ero ti args perni ena widget
        # print(lb_password_info.configure().keys())


    def login(self):
        pass

    def on_username_change_callback(self,event):
        pass

    def on_password_change_callback(self,event):
        if any(c.isupper() for c in self.password.get()):
            self.password_info.set("")
        else:
            self.password_info.set("Password should have one upper case")