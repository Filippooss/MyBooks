from tkinter import ttk, StringVar
import tkinter as tk


class EntryWithText(ttk.Frame):
    def __init__(
        self, master, title: str, var_entry: StringVar = None, entry_width: int = 20
    ):
        super().__init__(master=master)

        self.var_entry = var_entry if var_entry != None else StringVar()

        #'__' means private viriable

        self.__lb_title = ttk.Label(self, text=title)
        self.__entry = ttk.Entry(
            master=self, textvariable=self.var_entry, width=entry_width
        )

        # self.__entry.bind("<KeyRelease>", self.on_entry_change)

        self.__lb_title.pack(side="left", padx=(0, 10))
        self.__entry.pack(
            side="left",
        )

    # def on_entry_change(self,event) -> str:
    # return self.var_entry.get

    def get_value(self) -> str:
        return self.__entry.get()
