import tkinter as tk


class View(tk.Frame):
    def __init__(self, app,view_manager):
        super().__init__(master=app)
        self._app = app
        self._view_manager = view_manager
    
    def _display_view(self):
        raise NotImplementedError

    def _destroy_view(self):
        super().destroy()
