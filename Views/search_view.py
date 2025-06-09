import asyncio
import tkinter as tk
from threading import Thread
from tkinter import ttk

import api
import database
import Utility.save_manager as save_manager
from Models.book_model import Book
from Views.book_view import BookView
from Views.CustomWidgets.custom_notebook import CustomNotebook
from Views.CustomWidgets.entry_with_text import EntryWithText
from Views.CustomWidgets.search_result_template import SearchResultTemplate
from Views.CustomWidgets.vertical_scrolled_frame import (
    ScrollableFrame,
    VerticalScrolledFrame,
)
from Views.view import View
from tkinter.messagebox import showerror


class SearchView(View):

    SAVE_KEY = "searchview"
    def __init__(self,app,view_manager,args):
        super().__init__(app=app,view_manager=view_manager)
        self.max_books_display = 10
        self.var_search_bar = tk.StringVar()
        self.var_filter = tk.StringVar()
        #self.list_results = tk.Variable()
        self.search_results:list = list()
        self.save_dick=dict()

        #define widgets
        self.f_top=tk.Frame(self)
        self.lb_title = ttk.Label(self.f_top,text="Library",font=('Arial',40,'bold'))
        self.ewt_searchbar = EntryWithText(self.f_top,"Search Books",var_entry=self.var_search_bar,entry_width=50)
        self.bt_search = ttk.Button(self.f_top,text="Search",command=self.on_search)
        self.bt_search_online = ttk.Button(self.f_top ,text="Search Online",command=self.on_search_online)
        self.lb_filter=tk.Label(self.f_top,text="Select Filter")
        self.cbb_filters = ttk.Combobox(self.f_top,textvariable=self.var_filter,values=("None","Title","Author","Publisher"),state="readonly")
        self.vsf_results = VerticalScrolledFrame(self)

        self.cbb_filters.bind("<<ComboboxSelected>>",self.on_filter_selected)


        #config widgets
        self.bind('<MouseWheel>',lambda event : self.on_mouse_wheel(event))

        self.var_search_bar.trace_add("write",callback=self.on_searchbar_change_callback)

        #display
        self.f_top.pack(fill='y',expand=0,side="top")
        self.lb_title.grid(row=0,column=0,columnspan=4)
        self.cbb_filters.grid(row=1,column=0)
        self.ewt_searchbar.grid(row=1,column=1)
        self.bt_search.grid(row=1,column=2)
        self.bt_search_online.grid(row=1,column=3)

        #self.tabs.pack(fill='both',expand=1)
        self.vsf_results.pack(fill="both",expand=1)

        #add frames to tabs
        #self.tabs.add(self.vsf_results,text="Book Results")

        #load data
        self.save_dick = save_manager.read_temp_file(SearchView.SAVE_KEY)

        if self.save_dick.get("searchbar_text"):
            self.var_search_bar.set(self.save_dick["searchbar_text"])
        if self.save_dick.get("displayed_books"):
            serialized_books = self.save_dick["displayed_books"]
            for index,book_serialized in enumerate(serialized_books):
                book_model = Book.from_json(book_serialized)

                SearchResultTemplate(self.vsf_results.f_intirior,book_model,self.on_template_clicked,index,self._app.user.username)
                self.search_results.append(book_model)

        self.check_for_book()

        #set default filter
        self.cbb_filters.set("None")

    def on_search_online(self):
        self.vsf_results.delete_children()

        #self.search_results = asyncio.create_task(api.fetch_book_data(self.var_search_bar.get()))
        thread = SearchOnline(self.var_search_bar.get(),self.cbb_filters.get())
        thread.start()
        self.bt_search.config(state="disabled")
        self.bt_search_online.config(state="disabled")
        self.check_tread_result(thread)


    def check_tread_result(self,thread:Thread):
        if thread.is_alive():
            self.after(100,lambda: self.check_tread_result(thread))
        else:
            self.bt_search.config(state="enabled")
            self.bt_search_online.config(state="enabled")

            self.search_results = thread.result
            if len(self.search_results) < 1:
                return
            if type(self.search_results) == str:
                showerror("Error",self.search_results)
                return

            for index,book in enumerate(self.search_results):

                SearchResultTemplate(self.vsf_results.f_intirior,book,self.on_template_clicked,index,self._app.user.username)


    def on_search(self):
        #clear container
        self.vsf_results.delete_children()

        #1 search book local
        self.search_results:list = database.search_books(self.var_search_bar.get(),self._app.user.username)
        if len(self.search_results) < 1:
            self.vsf_results.show_message("No books found locally")
            return

        for index,book in enumerate(self.search_results):
            SearchResultTemplate(self.vsf_results.f_intirior,book,self.on_template_clicked,index,self._app.user.username)

    def on_filter_selected(self,event):
        self.cbb_filters.get()
        print(f"filter selected: {self.cbb_filters.get()}")

    def on_template_clicked(self,template_id:int):
        # serialized_books = []
        # for book in self.search_results:
        #     serialized_book = book.to_json()
        #     serialized_books.append(serialized_book)

        self.save_dick = {
            "searchbar_text":self.var_search_bar.get(),
            "displayed_books": [book.to_json() for book in self.search_results]
        }

        save_manager.write_temp_file(self.save_dick,SearchView.SAVE_KEY)

        book_model = self.search_results[template_id]
        self._view_manager.set_data_for_next_view(book = book_model)

        self._view_manager.change_view("BookView")

    def on_mouse_wheel(self,event):
        #https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar
        self.vsf_results.cv_container.yview_scroll(int(-1 * (event.delta/120)),"units")

    def on_searchbar_change_callback(self,*args):
        #TODO na tou emfanizi apotelesmata kathe fora pou pliktrologi kenourgio grama sto search bar
        pass

    def _display_view(self):
        self.pack(expand=1,fill="both")

    def _destroy_view(self):
        self.unbind("<KeyRelease>")
        return super()._destroy_view()

    def check_for_book(self,event=None):
        def on_retry():
            #TODO
            pass
        #exi proigithi load opote an i lista exi idi adikimena den kanoume tipota
        if len(self.search_results) > 0:
            return
        self.search_results:list = database.get_books(username=self._app.user.username)

        #prospathia na vri vivlia local
        if(len(self.search_results) > 0):
            for index,book in enumerate(self.search_results):
                    template = SearchResultTemplate(self.vsf_results.f_intirior,book,self.on_template_clicked,index,self._app.user.username)
        else:
            #an den vri vivlia vgazoume message

            #pername command gia na to ti tha kani sto retry
            self.vsf_results.show_message("No books",on_retry)



class SearchOnline(Thread):
    def __init__(self,input,filter_field):
        super().__init__(daemon=True) # daemon=True means the thread will exit when the main program exits
        self.result = None
        self.input = input
        self.filter_field = filter_field
    def run(self):
        self.result = api.fetch_book_data(self.input,self.filter_field)
