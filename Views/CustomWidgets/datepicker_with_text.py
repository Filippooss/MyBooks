from tkinter import ttk
import tkinter as tk
from tkcalendar import DateEntry


class DatepickerWithText (ttk.Frame):
    def __init__(self, master,title:str):
        super().__init__(master=master)
        
        #'__' means private viriable
        
        self.__lb_title = ttk.Label(self,text=title)
        self.__date_entry = DateEntry(self)


        self.__lb_title.pack(side="left",padx=(0,10))
        self.__date_entry.pack(side="right")

    def get_date_value(self) -> str:
        return self.__date_entry.get_date()