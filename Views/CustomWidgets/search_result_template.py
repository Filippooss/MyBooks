import io
import tkinter as tk
from tkinter import  ttk
from PIL import Image, ImageTk

from Models.book_model import Book
import database
from Utility import file_manager

class SearchResultTemplate(tk.Frame):
    def __init__(self,master,book_model:Book,on_event,template_id:int,username):
        super().__init__(master=master)
        self.config(bg="black",padx=5,pady=5)

        self.username = username
        self.book_model = book_model
        self.on_event = on_event
        self.template_id = template_id
        #self.grid(row=SearchResultTemplate.index,column=0)
        self.pack(anchor="w",padx=2,pady=2)
        #self.config()

        #define style for ttk
        add_raw = Image.open(file_manager.resource_path("Assets/bookmark_add_128_black.png"))
        add_raw = add_raw.resize((20,20),Image.Resampling.LANCZOS)
        self.tk_image_add = ImageTk.PhotoImage(add_raw)


        temp = Image.open(io.BytesIO(book_model.image_raw))
        temp = temp.resize((135,200))

        try:
            if not book_model.image_raw:
                raise ValueError("No image data")
            temp = Image.open(io.BytesIO(book_model.image_raw))
        except Exception as e:
            print(f"Could not load book image: {e}")
            temp = Image.open(file_manager.resource_path("Assets/no_image.png"))  # fallback image
        temp = temp.resize((135,200))
        self.image = ImageTk.PhotoImage(temp)
        
        #create widgets
        self.cv_image = tk.Canvas(self,width=temp.size[0],height=temp.size[1],borderwidth=0,highlightthickness=0)
        self.f_info = tk.Frame(self)
        self.lb_title = ttk.Label(self.f_info,text=book_model.title,style="new.TLabel",justify="left",wraplength=500)
        self.lb_author = ttk.Label(self.f_info,text=f'Author: {book_model.author}',style="new.TLabel",justify="left")
        self.bt_add_book = ttk.Button(self.f_info,image=self.tk_image_add,command=self.on_add_book)
        self.bt_inspect_book = ttk.Button(self.f_info,text="Read More",command=self.on_inspect_book)

        #configure image canva
        self.cv_image.create_image(0,0,anchor='nw',image=self.image)

        #display
        self.cv_image.pack(side="left")
        self.f_info.pack(side="left",fill="y")

        self.bt_add_book.pack(anchor="ne",pady=(0,40))
        self.lb_title.pack()
        self.lb_author.pack()
        self.bt_inspect_book.pack()


    def on_inspect_book(self):
        self.on_event(self.template_id)

    def on_add_book(self):
        add_raw = Image.open(file_manager.resource_path("Assets/bookmark_added_128_black.png"))
        add_raw = add_raw.resize((20,20),Image.Resampling.LANCZOS)
        self.tk_image_add = ImageTk.PhotoImage(add_raw)

        self.bt_add_book.config(image=self.tk_image_add)
        #TODO
        database.insert_book(self.book_model,self.username)
