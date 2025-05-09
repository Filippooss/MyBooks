import tkinter as tk
from tkinter import ttk
import database


class SignupView(tk.Frame):
    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master)

        self.view_manager = view_manager
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.re_password = tk.StringVar()


        #define widgets
        self.frame=ttk.Frame(self)
        self.title_label = ttk.Label(self.frame,text="Singup",font=('Arial',40,'bold'))
        self.lb_username = ttk.Label(self.frame,text='Enter Username' , font=('Arial',10))
        self.entry_username = ttk.Entry(self.frame, textvariable=self.username)
        self.lb_password = ttk.Label(self.frame,text='Enter Password',font=('Arial',10))
        self.entry_password = ttk.Entry(self.frame,textvariable=self.password)
        self.lb_re_password = ttk.Label(self.frame,text='Confirm Password',font=('Arial',10))
        self.entry_re_password = ttk.Entry(self.frame,textvariable=self.re_password)
        self.bt_signup = ttk.Button(self.frame,text="Sign up",command=lambda: self.on_sign_up())
        self.bt_login = ttk.Button(self.frame,text="Already have an account?",command=lambda: self.on_login())


        self.entry_password.bind("<KeyRelease>", self.on_password_change_callback)


        #display widgets
        self.title_label.pack(pady=(100,0))
        self.frame.pack(expand=1)
        self.lb_username.grid(row=1,column=0)
        self.entry_username.grid(row=1,column=1)
        self.lb_password.grid(row=2,column=0)
        self.entry_password.grid(row=2,column=1)
        self.lb_re_password.grid(row=3,column=0)
        self.entry_re_password.grid(row=3,column=1)
        self.bt_signup.grid(row=4,column=0,columnspan=2)
        self.bt_login.grid(row=5,column=0,columnspan=2)
    
    def on_login(self):
        self.view_manager.change_view('LoginView')

    def on_sign_up(self):
        if(self.password.get() == self.re_password.get()):
            print("o kodikos ine sostos")
            database.insert_user(self.username.get(),self.password.get())
            #self.view_manager.change_view()
        
    def on_password_change_callback(self,event):
        self.lb_password_info.config(foreground="black")

        if any(c.isupper() for c in self.password.get()):
            self.password_info.set("")
        elif self.password.get() == '':
            self.password_info.set("")
        else:
            self.password_info.set("Password should have one upper case")

    def display_view(self):
        self.pack(expand=True,fill="both")

    def destroy_view(self):
        super().destroy()

    

