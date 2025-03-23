import tkinter as tk

class ViewManager:
    #app:tk.Misc = None

    def __init__(self,app:tk.Misc):
        self.app = app
        pass

    @staticmethod
    def change_view(open_view:tk.Widget, new_view:tk.Widget):

        open_view.destroy()
        
        new_view.pack()


