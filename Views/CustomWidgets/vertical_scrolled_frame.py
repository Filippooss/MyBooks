import tkinter as tk
import tkinter.ttk as ttk

#https://coderslegacy.com/python/make-scrollable-frame-in-tkinter/
class VerticalScrolledFrame(ttk.Frame):
    def __init__(self,master):
        super().__init__(master=master)

                
        self.vscrollbar = ttk.Scrollbar(self,orient='vertical')
        self.cv_container = tk.Canvas(self,bd=0,highlightthickness=0)
        self.f_intirior = tk.Frame(self.cv_container,bg="red")


        #reset the view
        self.cv_container.xview_moveto(0)
        self.cv_container.yview_moveto(0)

        self.cv_container.configure(yscrollcommand=self.vscrollbar.set)
        self.vscrollbar.config(command=self.cv_container.yview)
        self.f_intirior.bind('<Configure>',self.configure_intirior)
        self.cv_container.bind('<Configure>',self.configure_canvas)
        #self.f_intirior.bind('<ListboxSelect>',self.on_item_click)


        self.window = self.cv_container.create_window((0,0),window = self.f_intirior,anchor ='nw' )

        #display items
        #self.f_intirior.pack(expand=1,fill="both",side="left")
        self.cv_container.pack(side='left',fill='both',expand=1)
        self.vscrollbar.pack(side='right',fill='y',expand=0)

    def configure_intirior(self,enent):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.f_intirior.winfo_reqwidth(),self.f_intirior.winfo_reqheight())
        self.cv_container.config(scrollregion=(0,0,size[0],size[1]))
        if self.f_intirior.winfo_reqwidth() != self.cv_container.winfo_reqwidth():
            # Update the canvas's width to fit the inner frame.
            self.cv_container.config(width=self.f_intirior.winfo_reqwidth())

    def configure_canvas(self,event):
        if self.f_intirior.winfo_reqwidth() != self.cv_container.winfo_reqwidth():
            # Update the inner frame's width to fill the canvas.
            self.cv_container.itemconfigure(self.window,width = self.cv_container.winfo_width())