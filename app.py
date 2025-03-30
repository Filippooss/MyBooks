import tkinter as tk
from Utility.view_manager import ViewManager

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #configure the root window
        self.title("MyBooks")
        self.geometry("420x420")

        app_icon = tk.PhotoImage(file='./Images/book.png')
        self.iconphoto(True,app_icon)
        self.config(background="#c3ddd7")

        # main window setup

        # menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        #
        self.file_menu = tk.Menu(self.menubar,tearoff=0)

        self.menubar.add_cascade(label="File",menu=self.file_menu)
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Add Book")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",command=quit)

if __name__ == "__main__":
    app = App()
    controller = ViewManager(app)
    #run
    app.mainloop()