import tkinter as tk
from tkinter import ttk,StringVar
from typing import Self
from Models.book_model import Book
from Views.view import View

class BookView(View):
    def __init__(self,master,view_manager):
        super().__init__(master=master,view_manager=view_manager)
    
        self.var_title = StringVar()
        self.var_author = StringVar()
        self.var_publisher = StringVar()
        self.var_description = StringVar()

        #define widgets
        self.lb_title = tk.Label(self,textvariable=self.var_title, font=("Arial",30))
        self.lb_author = tk.Label(self,textvariable=self.var_author)
        self.lb_publisher = tk.Label(self,textvariable=self.var_publisher)
        self.lb_description = tk.Label(self,textvariable=self.var_description)
        self.cv_image = tk.Canvas(self)

        #display widgets
        self.lb_title.pack()
        self.cv_image.pack(side="left")
        self.lb_author.pack()
        self.lb_publisher.pack()
        self.lb_description.pack()
    
    def _display_view(self):
        self.pack(fill="both",expand=1)

    def set_book_model(self,book_model:Book):
        self.book_model = book_model

        self.var_title.set(book_model.title)
        self.var_author.set(book_model.author)
        self.var_publisher.set(book_model.publisher)
        self.var_description.set(book_model.description)


if __name__ == "__main__":
    root = tk.Tk()

    book_model = Book(1,"a","b","ab",2000,"abc",2,None)
    debug_view = BookView(root,None,book_model)

    debug_view._display_view()

    root.mainloop()

