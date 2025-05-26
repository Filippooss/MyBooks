import tkinter as tk
from tkinter import ttk
from Models.user_model import User
from Views.view import View
import database
import Utility.save_manager as save_manager


class LoginView(View):
    def __init__(self,app,view_manager,args):
        super().__init__(app=app,view_manager=view_manager)

        user_data = save_manager.load("user")
        app_data = save_manager.load("app") 
        self.app = app

        self.var_password = tk.StringVar()
        self.var_username = tk.StringVar()
        self.var_password_info = tk.StringVar()
        self.var_save_credentials = tk.BooleanVar()

        # define widgets
        self.frame = ttk.Frame(self)
        self.lb_title = ttk.Label(self, text='Login', font=('Arial', 40,'bold'))
        self.lb_username = ttk.Label(self.frame,text='Enter Username' , font=('Arial',10))
        self.entry_username = ttk.Entry(self.frame, textvariable=self.var_username)
        self.lb_password = ttk.Label(self.frame,text='Enter Password',font=('Arial',10))
        self.entry_password = ttk.Entry(self.frame, show='*', textvariable=self.var_password)
        self.btn_login = ttk.Button(self.frame,text='Login', command=lambda: self.on_login())
        self.lb_password_info = ttk.Label(self.frame, textvariable=self.var_password_info)
        self.cb_save_credentials = ttk.Checkbutton(self.frame,text="Save Credentials",variable=self.var_save_credentials,command=self.on_save_credentials)
        self.bt_signup = ttk.Button(self.frame,text="Sign Up",command=lambda: self.navigate_to_signup_view())
        self.bt_skip_login = ttk.Button(self,text="Skip Login",command=self.on_skip_login)

        # events
        self.entry_username.bind("<KeyRelease>", self.on_username_change_callback)
        self.bind_all('<Return>',lambda event: self.on_enter_pressed(event))

        #display
        self.lb_title.pack(pady=(100,0))
        self.frame.pack(expand=1)
        self.lb_username.grid(row=1,column=0)
        self.entry_username.grid(row=1, column=1)
        self.lb_password.grid(row=2,column=0)
        self.entry_password.grid(row=2, column=1)
        self.cb_save_credentials.grid(row=3,column=0,columnspan=2)
        self.lb_password_info.grid(row=4, column=0,columnspan=2)
        self.btn_login.grid(row=5, column=0,columnspan=2)
        self.bt_signup.grid(row=6,column=0,columnspan=2)
        self.bt_skip_login.pack(side="bottom",anchor='e',padx=8,pady=8)

        self.entry_username.focus()

        #load data
        if(len(user_data) > 0):
            self.var_username.set(user_data["name"]) 
            self.var_password.set(user_data["password"]) 
        if(len(app_data) > 0):
            self.var_save_credentials.set(app_data["save_credentials"])


        # otan den 3ero ti args perni ena widget
        # print(lb_password_info.configure().keys())
    
    def on_enter_pressed(self,event):
        print("1")
        self.on_login()

    def navigate_to_signup_view(self):
        self._view_manager.change_view("SignupView")
    
    #define how this view is going to be displayed
    def _display_view(self):
        self.pack(fill='both',expand=1)
    

    def on_login(self):

        is_correct = database.login_user(self.var_username.get(),self.var_password.get())

        if is_correct :
            
            if(self.var_save_credentials):
                data = {
                    "name":self.var_username.get(),
                    "password":self.var_password.get()
                    }
                save_manager.save(data,"user")
            
            self.app.set_current_user(User(self.var_username.get(),self.var_password.get()))
            self._app.enable_add_book()
            self._view_manager.change_view("SearchView")
        else:
            self.lb_password_info.config(foreground="red")
            self.var_password_info.set("Username or Password are incorect")

    def on_skip_login(self):
        self._view_manager.change_view("SearchView")

    def on_save_credentials(self):
        save_data ={
            "save_credentials":self.var_save_credentials.get()
        }

        save_manager.save(save_data,"app")

    def on_username_change_callback(self,event):
        pass


