import tkinter as tk
from Views.login_view import LoginView
from Views.signup_view import SignupView
from Views.search_view import SearchView

class ViewManager:
    #app:tk.Misc = None

    def __init__(self,app:tk.Tk):
        self.app = app

        self.current_displayed_view = None

        #all views must be added here
        self.view_dick = {
            'SignupView':SignupView,
            'LoginView':LoginView,
            'SearchView':SearchView
        }

        #display the default view which is the login view
        self.current_displayed_view = self.view_dick['LoginView'](master=self.app,view_manager=self)
        self.current_displayed_view.display_view()

    def change_view(self,new_view):
        """ Destroys current open view and displays the new one """
        #create instase of the new view
 
        temp_view = self.view_dick[new_view](master=self.app,view_manager=self)
        

        self.current_displayed_view.destroy_view()
        self.current_displayed_view = temp_view
        self.current_displayed_view.display_view()



