import tkinter as tk

from Views.view import View
from Views.login_view import LoginView
from Views.signup_view import SignupView

class ViewManager:
    #app:tk.Misc = None

    def __init__(self,app:tk.Tk):
        self.app = app
        self.views:dict[View,View] = {}

        self.view_list:list[View] = [
            SignupView,
            LoginView
        ]

        for view_class in self.view_list:
            view = view_class(master=self.app,view_manager=self)
            self.views[view_class] = view

            #how to display the view
            #view.grid(pady=5,padx=5,sticky='nsew',row=0,column=0)
            view.pack(pady=5,padx=5,expand=True,fill="both")

        #display the view
        self.views[LoginView].tkraise()

    def change_view(self,new_view:type[View]):
        view = self.views[new_view]
        #open_view.destroy()




