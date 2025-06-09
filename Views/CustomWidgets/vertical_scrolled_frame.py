import tkinter as tk
from tkinter import ttk,StringVar

#https://coderslegacy.com/python/make-scrollable-frame-in-tkinter/
class VerticalScrolledFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)

        self.var_message = StringVar()

        self.vscrollbar = ttk.Scrollbar(self,orient='vertical')
        self.hscrollbar = ttk.Scrollbar(self,orient='horizontal')
        self.cv_container = tk.Canvas(self,bd=0,highlightthickness=0,bg="#edfcab",yscrollcommand=self.vscrollbar.set,
                                      xscrollcommand=self.hscrollbar.set)#apalo prasino
        self.f_intirior = tk.Frame(self.cv_container,bg="#fce2ab")#apalo kokkino
        self.f_message_box = tk.Frame(self.f_intirior)
        self.lb_message = ttk.Label(self.f_message_box,textvariable=self.var_message)
        self.bt_retry = ttk.Button(self.f_message_box,text="Retry")

        #reset the view
        self.cv_container.xview_moveto(0)
        self.cv_container.yview_moveto(0)

        self.vscrollbar.config(command=self.cv_container.yview)
        self.hscrollbar.config(command=self.cv_container.xview)

        # Create a frame inside the canvas which will be scrolled with it.
        self.f_intirior.bind('<Configure>',self.configure_intirior)
        self.cv_container.bind('<Configure>',self.configure_canvas)
        self.window = self.cv_container.create_window((0,0),window = self.f_intirior,anchor ='nw' )

        self.vscrollbar.pack(side='right',fill='y',expand=0)
        self.hscrollbar.pack(side='bottom',fill='x',expand=0)

        """Do not add things to cv_container"""
        self.cv_container.pack(side='left',fill='both',expand=1)

        #self.f_message_box.pack()


    def configure_intirior(self,enent):
        #print("Interior req width/height:", self.f_intirior.winfo_reqwidth(), self.f_intirior.winfo_reqheight())
        #print(f"intirior width:{self.f_intirior.winfo_width()},height: {self.f_intirior.winfo_height()}")
        #print(f"canvas requested width:{self.cv_container.winfo_reqwidth()},height: {self.cv_container.winfo_reqheight()}")
        #print("Canvas width/height:", self.cv_container.winfo_width(), self.cv_container.winfo_height())

        # Update the scrollbars to match the size of the inner frame.
        size = (self.f_intirior.winfo_reqwidth(),self.f_intirior.winfo_reqheight())
        self.cv_container.config(scrollregion=(0,0,size[0],size[1]))#left,top,right,bottom

        if(self.cv_container.winfo_reqheight() < self.f_intirior.winfo_height()):
            #self.f_intirior.configure(width=self.cv_container.winfo_width())
            pass


    def configure_canvas(self,event):
        #print("Interior req width/height:", self.f_intirior.winfo_reqwidth(), self.f_intirior.winfo_reqheight())
        #print(f"intirior width:{self.f_intirior.winfo_width()},height: {self.f_intirior.winfo_height()}")
        #print(f"canvas requested width:{self.cv_container.winfo_reqwidth()},height: {self.cv_container.winfo_reqheight()}")
        #print("Canvas width/height:", self.cv_container.winfo_width(), self.cv_container.winfo_height())

        #to kanoume auto oste an exoume kati mikrotero apo ton canva na kani stretch
        if self.f_intirior.winfo_reqwidth() < self.cv_container.winfo_width():
            self.cv_container.itemconfigure(self.window, width=self.cv_container.winfo_width())
        else:
            self.cv_container.itemconfigure(self.window, width=self.f_intirior.winfo_reqwidth())

    def get_is_empty(self) -> bool:
        return len(self.f_intirior.winfo_children()) < 1

    def delete_children(self) :
        for widget in self.f_intirior.winfo_children():
            widget.destroy()

    def show_message(self,message:str,command=None):
        self.delete_children()

        self.f_message_box.pack(fill="x",expand=1,anchor='center')
        self.lb_message.pack()
        self.bt_retry.pack()

        self.var_message.set(message)
        self.bt_retry.config(command=command)

class ScrollableFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        canvas = tk.Canvas(self,bg="#edfcab")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar_h = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.f_intirior = tk.Frame(canvas,bg="#fce2ab")

        self.f_intirior.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.f_intirior, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar_h.set)

        scrollbar_h.pack(side="bottom", fill="x")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

    def get_is_empty(self) -> bool:
        return len(self.f_intirior.winfo_children()) < 1

    def delete_children(self) :
        for widget in self.f_intirior.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    pass
