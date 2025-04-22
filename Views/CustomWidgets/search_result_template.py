import io
import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen

from PIL import Image, ImageTk


class SearchResultTemplate(tk.Frame):

    def __init__(self,master,title:str,image_url,author:str,on_event,template_id:int):
        super().__init__(master=master)

        self.on_event = on_event
        self.template_id = template_id
        #self.grid(row=SearchResultTemplate.index,column=0)
        self.pack(fill="both",padx=2,pady=2)
        self.config(bg="yellow")
        with urlopen(image_url) as u:
            raw_data = u.read()

        #define style for ttk

        temp = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image=temp)
        #create widgets
        self.cv_image = tk.Canvas(self,width=temp.size[0],height=temp.size[1],borderwidth=0,highlightthickness=0)
        self.f_info = tk.Frame(self,bg="green")
        self.lb_title = ttk.Label(self.f_info,text=title,style="new.TLabel",justify="left")
        self.lb_author = ttk.Label(self.f_info,text=f'Author: {author}',style="new.TLabel",justify="left")
        self.bt_inspect_book = ttk.Button(self.f_info,text="Reed More",command=self.on_inspect_book)

        #configure image canva
        self.cv_image.create_image(0,0,anchor='nw',image=self.image)

        #display
        self.cv_image.pack(side="left")
        self.f_info.pack(side="left",fill="none")

        self.lb_title.pack(side="top")
        self.lb_author.pack(side='top')
        self.bt_inspect_book.pack()

        
    def on_inspect_book(self):
        self.on_event(self.template_id)
            
        
