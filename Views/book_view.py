from logging import root
import tkinter as tk
from tkinter import ttk,StringVar
from Models.book_model import Book
from Views.view import View

class BookView(View):
    def __init__(self,master,view_manager, book_model:Book):
        super().__init__(master=master,view_manager=view_manager)
    
        self.book_model = book_model

        #define widgets
        self.lb_title = ttk.Label(self,text=book_model.title, style=("Arial",30))
        
    def _display_view(self):
        self.pack(fill="both",expand=1)
    
    def _destroy_view(self):
        return super()._destroy_view()
    

if __name__ == "__main__":
    root = tk.Tk()

    book_model = Book(1,"a","b","ab",2000,"abc",2,None)
    deubug_view = BookView(root,None,book_model)

    deubug_view.pack()

    root.mainloop()

