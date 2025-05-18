import tkinter as tk
from tkinter import messagebox
import database

class RatingWidget(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)

        self.rating = 0
        self.stars = []

        self.lb_title = tk.Label(self,text="Rate this book",font=("Arial",14))
        self.f_stars= tk.Frame(self)
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_rating)


        self.lb_title.pack(pady=10)
        self.f_stars.pack()

        for i in range(5):
            star = tk.Label(self.f_stars, text="☆", font=("Arial", 30), cursor="hand2")
            star.pack(side=tk.LEFT, padx=5)
            star.bind("<Enter>", lambda e, idx=i: self.on_hover(idx))
            star.bind("<Leave>", self.on_leave)
            star.bind("<Button-1>", lambda e, idx=i: self.set_rating(idx))
            self.stars.append(star)

        self.submit_button.pack(pady=10)

    def on_hover(self, index):
        for i in range(5):
            self.stars[i].config(text="★" if i <= index else "☆")

    def on_leave(self, event):
        for i in range(5):
            self.stars[i].config(text="★" if i < self.rating else "☆")

    def set_rating(self, index):
        self.rating = index + 1
        self.on_leave(None)

    def submit_rating(self):
        if self.rating == 0:
            messagebox.showwarning("No Rating", "Please select a rating before submitting.")
        else:
            messagebox.showinfo(f"You rated this book {self.rating} out of 5.")
            #apothikeusi tou rating
            