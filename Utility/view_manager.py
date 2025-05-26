from Views.add_book_view import AddBookView
from Views.book_view import BookView
from Views.login_view import LoginView
from Views.search_view import SearchView
from Views.signup_view import SignupView
from Views.view import View

class ViewManager:
    #app:tk.Misc = None

    def __init__(self,app,overide_view:str=None):
        self.app = app
        self.args = None
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
        self.current_displayed_view = self.view_dick['LoginView'](app=self.app,view_manager=self,args=self.args)
        if(overide_view != None): self.current_displayed_view = self.view_dick[overide_view](app=self.app,view_manager=self,args=self.args)
        self.current_displayed_view._display_view()
    
    def set_data_for_next_view(self,**kwargs):
        self.args = kwargs


    def change_view(self,new_view) -> None:
        """ Destroys current open view and displays the new one """
        #create instase of the new view
 
        temp_view = self.view_dick[new_view](app=self.app,view_manager=self,args=self.args)
        self.args = None
        
        self.current_displayed_view._destroy_view()
        self.current_displayed_view = temp_view
        self.current_displayed_view._display_view()

        return self.current_displayed_view



