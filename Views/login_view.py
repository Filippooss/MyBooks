import tkinter as tk
from tkinter import ttk


class LoginView(tk.Frame):
    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master)
        
        self.view_manager = view_manager

        self.password = tk.StringVar()
        self.username = tk.StringVar()
        self.password_info = tk.StringVar()


        # define widgets
        self.label = ttk.Label(self, text='Login', font=('Arial', 40,'bold'))
        self.lb_username = ttk.Label(self,text='Enter Username' , font=('Arial',10))
        self.entry_username = ttk.Entry(self, textvariable=self.username)
        self.lb_password = ttk.Label(self,text='Enter Password',font=('Arial',10))
        self.entry_password = ttk.Entry(self, show='*', textvariable=self.password)
        self.btn_login = ttk.Button(self,text='Login', command=lambda: self.login())
        self.lb_password_info = ttk.Label(self, textvariable=self.password_info)
        self.bt_signup = ttk.Button(self,text="Sign Up",command=lambda: self.navigate_to_signup_view())

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
        self.bt_signup.grid(row=5,column=0,columnspan=2)

        # otan den 3ero ti args perni ena widget
        # print(lb_password_info.configure().keys())

    def navigate_to_signup_view(self):
        self.view_manager.change_view("SignupView")
    
    #define how this view is going to be displayed
    def display_view(self):
        self.pack(pady=5,padx=5,expand=True,fill="both")

    def destroy_view(self):
        super().destroy()

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

