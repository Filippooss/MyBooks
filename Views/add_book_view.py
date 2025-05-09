import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from PIL import Image, ImageTk

import database
from Views.CustomWidgets.datepicker_with_text import DatepickerWithText
from Views.CustomWidgets.entry_with_text import EntryWithText
from Views.view import View


class AddBookView(View):
    def __init__(self,master,view_manager):
        super().__init__(master=master,view_manager=view_manager)
        
        

        #difine widgets
        self.title = ttk.Label(self,text="Add Book",font=('Arial', 40,'bold'))
        self.f_horizontal = ttk.Frame(self)

        self.f_right=ttk.Frame(self.f_horizontal)
        self.ewt_book_title = EntryWithText(self.f_right,title="Book Title:")
        self.ewt_book_author = EntryWithText(self.f_right,title="Book Author:")
        self.dp_book_release = DatepickerWithText(self.f_right,title="Book Release Date")
        self.lb_discription = ttk.Label(self.f_right,text="Book Discription:")
        self.txt_discription =tk.Text(self.f_right,height=8)

        self.f_left = tk.Frame(self.f_horizontal,background='red')
        self.bt_impor_image = ttk.Button(self.f_left,text="Import Book Cover",command=self.on_import_cover_image) 
        self.cv_image = tk.Canvas(self.f_left,borderwidth=0,highlightthickness=0,width=550,height=900,bg='blue')

        self.bt_add_book = ttk.Button(self,text="Add New Book",command=self.on_add_book)


        
        #display widgets
        self.title.pack()
        self.f_horizontal.pack(expand=1)

        self.f_left.pack(fill="none",expand=1,side="left")
        self.f_right.pack(fill="none",expand=1,side="left")

        self.ewt_book_title.pack(anchor='w',pady=(0,10))
        self.ewt_book_author.pack(anchor="w",pady=(0,10))
        self.dp_book_release.pack(anchor="w",pady=(0,10))
        self.lb_discription.pack(anchor="w")
        self.txt_discription.pack(pady=(0,10))
        
        self.cv_image.pack(anchor='w',expand=1,fill="both")
        self.bt_impor_image.pack(anchor="w")

        self.bt_add_book.pack(anchor="center")

    def on_add_book(self):

        #image_raw

        database.insert_book(self.ewt_book_title.get_value(),
                             self.ewt_book_author.get_value(),
                             self.dp_book_release.get_date_value(),
                             ""
                             )

    def on_import_cover_image(self):
        image_path:str = fd.askopenfilename(title="Import Book Cover",filetypes=(("png files","*.png"),("jpeg files","*.jpeg"),("jpg files","*.jpg")),initialdir='/')
        print(image_path)

        if image_path == "":
            return

        image:Image = Image.open(image_path)
        image = image.resize((550,900))
        self.tk_image  = ImageTk.PhotoImage(image)

        #self.cv_image.config(width=image.size[0],height=image.size[1])
        #self.cv_image.config(width=500,height=500)
        self.cv_image.create_image(0,0,anchor="nw",image=self.tk_image)


    def display_view(self):
        self.pack(expand=True,fill="both")
