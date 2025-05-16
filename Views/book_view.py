import io
import tkinter as tk
from tkinter import ttk,StringVar
from typing import Self

from PIL import Image,ImageTk
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
        self.f_right = ttk.Frame(self)
        self.lb_title = tk.Label(self.f_right,textvariable=self.var_title, font=("Arial",30))
        self.lb_author = tk.Label(self.f_right,textvariable=self.var_author)
        self.lb_publisher = tk.Label(self.f_right,textvariable=self.var_publisher)
        self.lb_description = tk.Label(self.f_right,textvariable=self.var_description)
        self.cv_image = tk.Canvas(self)
        self.bt_back = ttk.Button(self,text="Back",command=self.on_back)

        #display widgets
        self.lb_title.pack()
        self.bt_back.pack(side="top",anchor="w")
        self.cv_image.pack(side="left")
        self.f_right.pack(side="left",fill="none",expand=0)
        self.lb_author.pack()
        self.lb_publisher.pack()
        self.lb_description.pack()

    def on_back(self):
        self._view_manager.change_view("SearchView")
    
    def _display_view(self):
        self.pack(fill="both",expand=1)

    def set_book_model(self,book_model:Book):
        self.book_model = book_model

        # self.var_title.set(book_model.title)
        # self.var_author.set(book_model.author)
        # self.var_publisher.set(book_model.publisher)
        # self.var_description.set(book_model.description)
        self.var_title.set("Titlos vivliou")
        self.var_author.set("Author vivliou")
        self.var_publisher.set("Publisher vivliou")
        self.var_description.set("Description vivliou sdfisdufiodshfgiuklsdfahgkjsdfhlak")
        
        temp = Image.open(io.BytesIO(book_model.image_raw))
        temp = temp.resize((135,200))
        self.image = ImageTk.PhotoImage(image=temp)
        self.cv_image.create_image(0,0,image=self.image,anchor="nw")


if __name__ == "__main__":
    root = tk.Tk()

    book_model = Book(1,"a","b","ab",2000,"abc",2,None)
    debug_view = BookView(root,None,book_model)

    debug_view._display_view()

    root.mainloop()

