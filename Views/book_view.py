import io
import tkinter as tk
from tkinter import ttk,StringVar
from Views.CustomWidgets.rating_widget import RatingWidget

from PIL import Image,ImageTk
from Models.book_model import Book
from Views.view import View

class BookView(View):
    def __init__(self,app,view_manager):
        super().__init__(app=app,view_manager=view_manager)
    
        self.var_title = StringVar()
        self.var_author = StringVar()
        self.var_publisher = StringVar()
        self.var_description = StringVar()

        #define widgets
        self.f_horizontal = tk.Frame(self)
        self.f_right = tk.Frame(self.f_horizontal)
        self.f_left = tk.Frame(self.f_horizontal)
        self.lb_title = tk.Label(self.f_right,textvariable=self.var_title, font=("Arial",30))
        self.lb_author = tk.Label(self.f_right,textvariable=self.var_author)
        self.lb_publisher = tk.Label(self.f_right,textvariable=self.var_publisher)
        self.lb_description = tk.Label(self.f_right,textvariable=self.var_description)
        self.cv_image = tk.Canvas(self.f_left,width=400,height=550)
        self.bt_back = ttk.Button(self,text="Back",command=self.on_back)
        self.rating_widget = RatingWidget(self.f_left)

        #display widgets
        self.lb_title.pack()
        self.f_horizontal.pack(fill="both",expand=1)
        self.f_left.pack(side="left",fill="both",expand=0)  
        self.f_right.pack(side="left",fill="both",expand=0)
        self.bt_back.pack(side="top",anchor="w")
        self.cv_image.pack(fill="none",expand=0)
        self.lb_author.pack()
        self.lb_publisher.pack()
        self.lb_description.pack()

        self.rating_widget.pack()

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
        temp = temp.resize((400,550))
        self.image = ImageTk.PhotoImage(image=temp)
        self.cv_image.create_image(0,0,image=self.image,anchor="nw")


if __name__ == "__main__":
    root = tk.Tk()

    book_model = Book(1,"a","b","ab",2000,"abc",2,None)
    debug_view = BookView(root,None,book_model)

    debug_view._display_view()

    root.mainloop()

