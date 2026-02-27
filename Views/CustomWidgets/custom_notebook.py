import tkinter as tk
from tkinter import ttk

from Views.view import View


class CustomNotebook(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master=master)

        # self.nt_tabs= ttk.Notebook(self)

        self.bind("<B1-Motion>", self.reorder)

        # self.nt_tabs.pack(fill='both',expand=1)

    def reorder(self, event):
        try:
            index = self.index(f"@{event.x},{event.y}")
            self.insert(index, child=self.select())
        except tk.TclError:
            pass
