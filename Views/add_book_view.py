import io
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from PIL import Image, ImageTk

from Models.book_model import Book
import database
from Views.CustomWidgets.datepicker_with_text import DatepickerWithText
from Views.CustomWidgets.entry_with_text import EntryWithText
from Views.view import View


class AddBookView(View):
    def __init__(self,app,view_manager,args):
        super().__init__(app=app,view_manager=view_manager)
        
        

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
        self.bt_import_image = ttk.Button(self.f_left,text="Import Book Cover",command=self.on_import_cover_image) 
        self.bt_no_image = ttk.Button(self.f_left,text="No Image",command=self.on_no_image)
        self.cv_image = tk.Canvas(self.f_left,borderwidth=0,highlightthickness=0,width=450,height=600,bg='blue')

        self.bt_add_book = ttk.Button(self.f_right,text="Add New Book",command=self.on_add_book)


        
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
        self.bt_import_image.pack(side="left",anchor="center")
        self.bt_no_image.pack(side="left",anchor='center')

        self.bt_add_book.pack()

    def on_add_book(self):
        #image_raw
        buffer = io.BytesIO()
        self.image.save(buffer,format="PNG")
        
        book = Book(
            id=0,
            title=self.ewt_book_title.get_value(),
            author=self.ewt_book_author.get_value(),
            description=self.txt_discription.get("1.0",tk.END),
            image_raw=buffer.getvalue(),
            release_year=self.dp_book_release.get_date_value(),
            version=-1,
            publisher="abc",
        )
        database.insert_book(book,self._app.user.username)
        #TODO: elenxos an i kataxorisi itan epitixis kai meta alagi tou view
        self._view_manager.change_view("LoginView")
                             

    def on_no_image(self):
        image_path = "./Assets/TheSumofAllThings_cover.jpg"

        temp_emage = Image.open(image_path)
        self.image = temp_emage.resize((450,600))
        self.tk_image  = ImageTk.PhotoImage(self.image)
        
        self.cv_image.create_image(0,0,anchor="nw",image=self.tk_image)

    def on_import_cover_image(self):
        image_path:str = fd.askopenfilename(title="Import Book Cover",filetypes=(("png files","*.png"),("jpeg files","*.jpeg"),("jpg files","*.jpg")),initialdir='/')
        

        if image_path == "":
            print("No cover")
            return

        book_cover = Image.open(image_path)
        self.image = book_cover.resize((450,600), resample=Image.Resampling.LANCZOS)
        self.tk_image  = ImageTk.PhotoImage(self.image)

        #self.cv_image.config(width=image.size[0],height=image.size[1])
        #self.cv_image.config(width=500,height=500)
        self.cv_image.create_image(0,0,anchor="nw",image=self.tk_image)


    def _display_view(self):
        self.pack(expand=True,fill="both")

    def _destroy_view(self):
        return super()._destroy_view()
