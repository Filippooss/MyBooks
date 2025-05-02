import tkinter as tk
from Utility.view_manager import ViewManager

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.view_manager = ViewManager(self)

        #configure the root window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print(screen_width)
        self.title("MyBooks")
        self.geometry(f"420x420+{int(screen_width/2 - 700/2)}+{int(screen_height/2 - 700/2)}")
        self.minsize(700,700)

        app_icon = tk.PhotoImage(file='./Images/book.png')
        self.iconphoto(True,app_icon)
        self.config()
        
        # main window setup
        
        # menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        #
        self.file_menu = tk.Menu(self.menubar,tearoff=0)

        self.menubar.add_cascade(label="File",menu=self.file_menu)
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Add Book",command=self.on_add_book)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Log out",command=lambda: self.on_log_out())
        self.file_menu.add_command(label="Exit",command=lambda: self.quit())

    def on_log_out(self):
        self.view_manager.change_view("LoginView")
    
    def on_add_book(self):
        self.view_manager.change_view("AddBookView")

if __name__ == "__main__":
    app = App()
    #run
    app.mainloop()