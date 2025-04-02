import tkinter as tk
from tkinter import ttk
from api import get_info
from Views.CustomWidgets.search_result_template import SearchResultTemplate

class SearchView(tk.Frame):
    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master)

        self.view_manager = view_manager

        self.search_bar_text = tk.StringVar()
        self.list_results = tk.Variable()

        #define widgets
        self.f_top=ttk.Label(self)
        self.lb_title = ttk.Label(self.f_top,text="Library",font=('Arial',40,'bold'))
        self.lb_searchbar = ttk.Label(self.f_top,text='Search Books',font=("Arial"))
        self.entry_searchbar = ttk.Entry(self.f_top,textvariable=self.search_bar_text)
        self.cv_container = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self.cv_container,orient='vertical')
        self.bt_search = ttk.Button(self.f_top,text="Search",command=lambda:self.on_search())
        self.f_results_container = ttk.Frame(self.cv_container)

        self.cv_container.configure(yscrollcommand=self.scrollbar.set)
        self.cv_container.bind('<Configure>',lambda event: self.cv_container.configure(scrollregion=self.cv_container.bbox("all")))
        self.entry_searchbar.bind("<KeyRelease>",lambda event: self.on_searchbar_change_callback(event))
        #self.lbx_results_container.bind('<ListboxSelect>',self.on_item_click)

        #add new windows to canvas
        self.cv_container.create_window((0,0),window = self.f_results_container,anchor ='nw' )


        self.scrollbar.config(command=self.cv_container.yview)

        self.f_top.pack(fill='y',expand=False,side="top")
        #display
        self.lb_title.grid(row=0,column=0,columnspan=3)
        self.lb_searchbar.grid(row=1,column=0)
        self.entry_searchbar.grid(row=1,column=1)
        self.bt_search.grid(row=1,column=2)
        self.cv_container.pack(side='left',fill='both',expand=1)
        self.scrollbar.pack(side='right',fill='y')

    def on_search(self):
        search_result = get_info(self.search_bar_text.get())
        index = 1
        for book in search_result:
            titlos = book['Τίτλος']
            image_url = book['Εξώφυλλο']

            template = SearchResultTemplate(master=self.f_results_container,title=titlos,image_url=image_url)
            

            index += 1

    def on_item_click(self,event):
        pass        

    def on_searchbar_change_callback(self,event):
        pass

    def display_view(self):
        self.pack(expand=1,fill="both")


         