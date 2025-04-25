from tkinter import ttk
import tkinter as tk

class EntryWithText (ttk.Frame):
    def __init__(self, master,title:str):
        super().__init__(master=master)
        
        #'__' means private viriable
        
        self.__lb_title = ttk.Label(self,text=title)
        self.__entry = ttk.Entry(self)


        self.__lb_title.pack(side="left",padx=(0,10))
        self.__entry.pack(side="right")

    def get_value(self) -> str:
        return self.__entry.get()






    
