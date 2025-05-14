from email import message
import tkinter as tk
from tkinter import ttk,StringVar
from Views.view import View
import database
from Views.CustomWidgets.entry_with_text import EntryWithText


class SignupView(View):
    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master,view_manager=view_manager)

        self.is_password_valid:bool = False
        self.is_username_valid:bool = False

        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_repassword = StringVar()
        self.var_password_info = StringVar()
        self.var_repassword_info = StringVar()


        #define widgets
        self.frame=ttk.Frame(self)
        self.title_label = ttk.Label(self,text="Singup",font=('Arial',40,'bold'))
        self.ewt_username = EntryWithText(self.frame,"Enter Username",var_entry=self.var_username)
        self.ewt_password = EntryWithText(self.frame,"Enter Password",var_entry=self.var_password)
        self.ewt_repassword = EntryWithText(self.frame,"Confirm Password",var_entry=self.var_repassword)
        self.bt_signup = ttk.Button(self.frame,text="Sign up",command=lambda: self.on_sign_up())
        self.bt_login = ttk.Button(self.frame,text="Already have an account?",command=lambda: self.on_login())
        self.lb_password_info = ttk.Label(self.frame,textvariable=self.var_password_info,foreground="red")
        self.lb_repassword_info = ttk.Label(self.frame,textvariable=self.var_repassword_info,foreground="red")

        self.var_password.trace_add("write",callback=self.on_password_change_callback)
        self.var_repassword.trace_add("write",callback=self.on_repassword_change_callback)
        self.var_username.trace_add("write",callback=self.on_username_change_callback)
        #display widgets
        self.title_label.pack(pady=(100,0))
        self.frame.pack(expand=1)
        self.ewt_username.grid(row=1,columnspan=2)
        self.ewt_password.grid(row=2,columnspan=2)
        self.ewt_repassword.grid(row=4,columnspan=2)
        self.bt_signup.grid(row=6,column=0,columnspan=2)
        self.bt_login.grid(row=7,column=0,columnspan=2)
        
    def on_login(self):
        self._view_manager.change_view('LoginView')

    def on_sign_up(self):
        if (self.ewt_password.get_value() == self.ewt_repassword.get_value() and 
            self.is_password_valid == True and
            self.is_username_valid == True):

            print("o kodikos ine sostos")
            database.insert_user(self.ewt_username.get_value(),self.ewt_password.get_value())
            #self.view_manager.change_view()
        else:
            print("Cant sign up")
    def on_username_change_callback(self,*args):
        self.is_username_valid == False if len(self.var_username.get()) == 0 else True
       
    def on_password_change_callback(self,*args):
        def hide_message():
            self.var_password_info.set("")
            self.lb_password_info.grid_forget() 

        reasons = []
        if self.var_password.get() == '':
            hide_message()
            return
        
        if not any(c.isupper() for c in self.var_password.get()):
            reasons.append("Password should have one upper case.")
        if not any(c.isdigit() for c in self.var_password.get()):
            reasons.append("Password should have one digit.")
            
        if not reasons:
            hide_message()
            self.is_password_valid = True
            return

        self.lb_password_info.grid(row=3,columnspan=2)
        message = "\n".join(reasons)
        self.var_password_info.set(message)
        self.is_password_valid = False
        
        self.check_codes_same()

    def on_repassword_change_callback(self,*args):
        self.check_codes_same()

    def check_codes_same(self):
        if self.var_password.get() != self.var_repassword.get():
            self.lb_repassword_info.grid(row=5,columnspan=2)
            self.var_repassword_info.set("Passwords does not match")
            self.is_password_valid = False
            return
        else:
            self.is_password_valid = True
        
        if self.var_password.get() == '' and self.var_repassword == '':
            self.lb_repassword_info.grid_forget()

        self.lb_repassword_info.grid_forget()

        
    def _display_view(self):
        self.pack(expand=True,fill="both")

    

