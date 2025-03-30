import tkinter as tk

class View(tk.Frame):
    def __init__(self,master,view_manager):
        super().__init__(master=master)

        self.view_manager = view_manager

    def display(self):
        self.pack()

