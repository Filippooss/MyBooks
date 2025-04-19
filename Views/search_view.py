import tkinter as tk
from tkinter import ttk

from api import get_info
from Views.CustomWidgets.search_result_template import SearchResultTemplate
from Views.CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame


class SearchView(tk.Frame):
    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master)

        self.view_manager = view_manager

        self.search_bar_text = tk.StringVar()
        self.list_results = tk.Variable()
        self.search_results = {}

        #define widgets
        self.f_top=ttk.Label(self)
        self.lb_title = ttk.Label(self.f_top,text="Library",font=('Arial',40,'bold'))
        self.lb_searchbar = ttk.Label(self.f_top,text='Search Books',font=("Arial"))
        self.entry_searchbar = ttk.Entry(self.f_top,textvariable=self.search_bar_text)
        self.bt_search = ttk.Button(self.f_top,text="Search",command=self.on_search)
        self.vsf_results = VerticalScrolledFrame(master=self)


        #config widgets
        self.bind_all('<MouseWheel>',lambda event : self.on_mouse_wheel(event))

        self.entry_searchbar.bind("<KeyRelease>",lambda event: self.on_searchbar_change_callback(event))

        #display
        self.f_top.pack(fill='y',expand=False,side="top")
        self.lb_title.grid(row=0,column=0,columnspan=3)
        self.lb_searchbar.grid(row=1,column=0)
        self.entry_searchbar.grid(row=1,column=1)
        self.bt_search.grid(row=1,column=2)
        self.vsf_results.pack(fill="both",expand=1)


    def on_search(self):
        self.search_results = get_info(self.search_bar_text.get())
        index = 0
        for book in self.search_results:
            titlos = book['Τίτλος']
            image_url = book['Εξώφυλλο']
            author = book["Συγγραφέας"]

            template = SearchResultTemplate(self.vsf_results.f_intirior,titlos,image_url,author,self.on_template_clicked,index)

            index += 1

    def on_template_clicked(self,template_id):
        print(self.search_results[0])

    def on_mouse_wheel(self,event):
        #https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        self.vsf_results.cv_container.yview_scroll(int(-1 * (event.delta/120)),"units")   

    def on_searchbar_change_callback(self,event):
        pass

    def display_view(self):
        self.pack(expand=1,fill="both")

    def destroy_view(self):
        super().destroy()


         