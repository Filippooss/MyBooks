import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from urllib.request import urlopen
import io

class SearchResultTemplate(ttk.Frame):
    def __init__(self,master,title:str,image_url):
        super().__init__(master=master)
        
        self.pack()

        with urlopen(image_url) as u:
            raw_data = u.read()

        temp = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image=temp)
        #create widgets
        self.cv_image = tk.Canvas(self)
        self.title = ttk.Label(self,text=title)


        #configure iamge canva
        self.cv_image.create_image(10,10,anchor='nw',image=self.image)


        #display
        self.title.pack()
        self.cv_image.pack()
