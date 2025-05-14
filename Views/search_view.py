import tkinter as tk
from tkinter import ttk
from Models.book_model import Book
from Views.view import View
import api 
import database
from Views.CustomWidgets.search_result_template import SearchResultTemplate
from Views.CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame,ScrollableFrame
from Views.CustomWidgets.custom_notebook import CustomNotebook

class SearchView(View):

    def __init__(self,master:tk.Misc,view_manager):
        super().__init__(master=master,view_manager=view_manager)
        self.max_books_display = 10
        self.search_bar_text = tk.StringVar()
        self.list_results = tk.Variable()
        self.search_results:dict = dict()

        #define widgets
        self.f_top=ttk.Label(self)
        self.lb_title = ttk.Label(self.f_top,text="Library",font=('Arial',40,'bold'))
        self.lb_searchbar = ttk.Label(self.f_top,text='Search Books',font=("Arial"))
        self.entry_searchbar = ttk.Entry(self.f_top,textvariable=self.search_bar_text)
        self.bt_search = ttk.Button(self.f_top,text="Search",command=self.on_search)
        self.vsf_results = VerticalScrolledFrame(self)
        


        #config widgets
        self.bind_all('<MouseWheel>',lambda event : self.on_mouse_wheel(event))

        self.entry_searchbar.bind("<KeyRelease>",lambda event: self.on_searchbar_change_callback(event))

        #display
        self.f_top.pack(fill='y',expand=0,side="top")
        self.lb_title.grid(row=0,column=0,columnspan=3)
        self.lb_searchbar.grid(row=1,column=0)
        self.entry_searchbar.grid(row=1,column=1)
        self.bt_search.grid(row=1,column=2)
        #self.tabs.pack(fill='both',expand=1)
        self.vsf_results.pack(fill="both",expand=1)

        #add frames to tabs
        #self.tabs.add(self.vsf_results,text="Book Results")

        
        self.check_for_book()



    def on_search(self):
        #clear container
        self.vsf_results.delete_children()

        #1 search book local
        self.search_results = database.search_books(self.search_bar_text.get())
        if len(self.search_results) < 1:
            #Else search online
            self.search_results = api.fetch_book_data(self.search_bar_text.get())
            if len(self.search_results) < 1:
                return

        for index,book in enumerate(self.search_results):
            SearchResultTemplate(self.vsf_results.f_intirior,book,self.on_template_clicked,index)

    def on_template_clicked(self,template_id:int):
        print(template_id)

    def on_mouse_wheel(self,event):
        #https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        self.vsf_results.cv_container.yview_scroll(int(-1 * (event.delta/120)),"units")   

    def on_searchbar_change_callback(self,event):
        pass

    def _display_view(self):
        self.pack(expand=1,fill="both")

    def check_for_book(self,event=None):
        def on_retry():
            pass
        
        self.search_results = database.get_books()
        
        #prospathia na vri vivlia local
        if(len(self.search_results) > 0):
            for index,book in enumerate(self.search_results):
                    template = SearchResultTemplate(self.vsf_results.f_intirior,book,self.on_template_clicked,index)    
        else:
            #pername command gia na to ti tha kani sto retry
            self.vsf_results.show_message("No books",on_retry)





         