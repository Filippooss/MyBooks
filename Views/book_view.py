import io
import tkinter as tk
from tkinter import StringVar, ttk

from PIL import Image, ImageTk
from numpy.random import f

from Models.book_model import Book
from Views.CustomWidgets.rating_widget import RatingWidget
from Views.CustomWidgets.rating_canvas import RatingCanvas
from Views.view import View
from Views.CustomWidgets.vertical_scrolled_frame import VerticalScrolledFrame


class BookView(View):
    def __init__(self, app, view_manager, args: dict):
        super().__init__(app=app, view_manager=view_manager)

        self.book_model = args["book"]
        self.var_title = StringVar(value=f"Title: {self.book_model.title}")
        self.var_author = StringVar(value=f"Author: {self.book_model.author}")
        self.var_publisher = StringVar(value=f"Publisher: {self.book_model.publisher}")
        self.var_description = StringVar(
            value=f"Description: {self.book_model.description}"
        )

        # define widgets
        self.vcf = VerticalScrolledFrame(self)
        self.f_right = tk.Frame(self.vcf.f_intirior)
        self.f_left = tk.Frame(self.vcf.f_intirior)

        self.lb_title = tk.Label(
            self.f_right,
            textvariable=self.var_title,
            font=("Arial", 25),
            wraplength=300,
        )
        self.lb_author = tk.Label(self.f_right, textvariable=self.var_author)
        self.lb_publisher = tk.Label(self.f_right, textvariable=self.var_publisher)
        self.lb_description = tk.Label(
            self.f_right, textvariable=self.var_description, wraplength=500
        )

        self.cv_image = tk.Canvas(self.f_left, width=400, height=550)
        self.bt_back = ttk.Button(self.f_left, text="Back", command=self.on_back)
        self.rating_widget = RatingWidget(
            self.f_left, self.book_model, username=self._app.user.username
        )
        self.rating_canvas = RatingCanvas(self.f_left, self.book_model.title)

        # display widgets
        self.lb_title.pack()
        self.vcf.pack(fill="both", expand=1)
        self.f_left.pack(side="left", fill="both", expand=1)
        self.f_right.pack(side="left", fill="both", expand=1)
        self.cv_image.pack(fill="none", expand=0)
        self.lb_author.pack()
        self.lb_publisher.pack()
        self.lb_description.pack()

        self.rating_widget.pack()
        self.rating_canvas.pack()
        self.bt_back.pack(anchor="w")

        # set image
        temp = Image.open(io.BytesIO(self.book_model.image_raw))
        temp = temp.resize((400, 550))
        self.image = ImageTk.PhotoImage(image=temp)
        self.cv_image.create_image(0, 0, image=self.image, anchor="nw")

    def on_back(self):
        self._view_manager.change_view("SearchView")

    def _display_view(self):
        self.pack(fill="both", expand=1)


# TODO : add a button to let the user remove the book from his library

if __name__ == "__main__":
    root = tk.Tk()

    book_model = Book(1, "a", "b", "ab", 2000, "abc", 2, None)
    debug_view = BookView(root, None, book_model)

    debug_view._display_view()

    root.mainloop()
