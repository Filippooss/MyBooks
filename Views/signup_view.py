from tkinter import *
from Views.view import View


class SignupView(View):
    def __init__(self,master:Misc,view_manager):
        super().__init__(master=master,view_manager=view_manager)

    #child can override parents display
    #def display(self):
        #pass

