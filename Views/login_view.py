from tkinter import *
from .view import View

class LoginView(View):
    def __init__(self,master:Misc,view_manager):
        super().__init__(master)
        
        self.view_manager = view_manager

        #display frame
        #self.grid(pady=5,padx=5,sticky='nsew',row=0,column=0)
        self.password = StringVar()
        self.username = StringVar()
        self.password_info = StringVar()

        # define widgets

        self.label = Label(self, text='Login', font=('Arial', 40, 'bold'))
        self.lb_username = Label(self,text='Enter Username' , font=('Arial',10),padx=0,pady=0)
        self.entry_username = Entry(self, textvariable=self.username)
        self.lb_password = Label(self,text='Enter Password',font=('Arial',10))
        self.entry_password = Entry(self, show='*', textvariable=self.password)
        self.btn_login = Button(self,text='Login', command=lambda: self.login(), state=ACTIVE)
        self.lb_password_info = Label(self, justify=LEFT, textvariable=self.password_info)
        self.bt_create_account = Button(self,text="Sign Up",command=lambda: self.navigate_to_signup_view())

        # events
        self.entry_username.bind("<KeyRelease>", self.on_username_change_callback)
        self.entry_password.bind("<KeyRelease>", self.on_password_change_callback)

        #display
        self.label.grid(row=0, column=0,columnspan=2)
        self.lb_username.grid(row=1,column=0)
        self.entry_username.grid(row=1, column=1)
        self.lb_password.grid(row=2,column=0)
        self.entry_username.focus()
        self.entry_password.grid(row=2, column=1)
        self.btn_login.grid(row=4, column=0,columnspan=2)
        self.lb_password_info.grid(row=3, column=0,columnspan=2)
        self.bt_create_account.grid(row=5,column=0,columnspan=2)

        # otan den 3ero ti args perni ena widget
        # print(lb_password_info.configure().keys())

    def navigate_to_signup_view(self):
        #self.view_manager.change_view()
        pass

    
    def login(self):
        pass

    def on_username_change_callback(self,event):
        pass

    def on_password_change_callback(self,event):
        if any(c.isupper() for c in self.password.get()):
            self.password_info.set("")
        elif self.password.get() == '':
            self.password_info.set("")
        else:
            self.password_info.set("Password should have one upper case")

