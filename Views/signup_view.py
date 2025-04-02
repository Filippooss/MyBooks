import tkinter as tk
from tkinter import ttk


class SignupView(tk.Frame):
    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master)

        self.view_manager = view_manager
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.re_password = tk.StringVar()


        #define widgets
        self.title_label = ttk.Label(self,text="Singup",font=('Arial',40,'bold'))
        self.lb_username = ttk.Label(self,text='Enter Username' , font=('Arial',10))
        self.entry_username = ttk.Entry(self, textvariable=self.username)
        self.lb_password = ttk.Label(self,text='Enter Password',font=('Arial',10))
        self.entry_password = ttk.Entry(self,textvariable=self.password)
        self.lb_re_password = ttk.Label(self,text='Confirm Password',font=('Arial',10))
        self.entry_re_password = ttk.Entry(self,textvariable=self.re_password)
        self.bt_signup = ttk.Button(self,text="Sign up",command=lambda: self.on_sign_up())
        self.bt_login = ttk.Button(self,text="Already have an account?",command=lambda: self.on_login())

        #display widgets
        self.title_label.grid(row=0,column=0,columnspan=2)
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
            #self.view_manager.change_view()
        


    def display_view(self):
        self.pack(pady=5,padx=5,expand=True,fill="both")

    def destroy_view(self):
        super().destroy()

    

