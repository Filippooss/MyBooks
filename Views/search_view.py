import tkinter as tk
from tkinter import ttk

class SearchView(tk.Frame):
    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master)

        self.view_manager = view_manager

        