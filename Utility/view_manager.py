import tkinter as tk
from Views.add_book_view import AddBookView
from Views.login_view import LoginView
from Views.signup_view import SignupView
from Views.search_view import SearchView
from Views.book_view import BookView
from Views.view import View

class ViewManager:
    #app:tk.Misc = None

    def __init__(self,app:tk.Tk,overide_view:str=None):
        self.app = app

        self.current_displayed_view:View = None

            

        #all views must be added here
        self.view_dick = {
            'SignupView':SignupView,
            'LoginView':LoginView,
            'SearchView':SearchView,
            "AddBookView":AddBookView,
            "BookView":BookView
        }
            

        #display the default view which is the login view
        self.current_displayed_view = self.view_dick['LoginView'](master=self.app,view_manager=self)
        if(overide_view != None): self.current_displayed_view = self.view_dick[overide_view](master=self.app,view_manager=self)
        self.current_displayed_view._display_view()

    def change_view(self,new_view) -> None:
        """ Destroys current open view and displays the new one """
        #create instase of the new view
 
        temp_view = self.view_dick[new_view](master=self.app,view_manager=self)
        
        self.current_displayed_view._destroy_view()
        self.current_displayed_view = temp_view
        self.current_displayed_view._display_view()

        return self.current_displayed_view



