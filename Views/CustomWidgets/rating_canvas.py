import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import database
#import numpy as np


class RatingCanvas(tk.Frame):
    def __init__(self, master, title):
        super().__init__(master=master)
        #self.counts = np.array([], dtype=int)
        self.book_ratings = [0,0,0,0,0]
        self.get_ratings(title)

        canvas = FigureCanvasTkAgg(self.plot_ratings(),master=self)
        canvas.draw()

        canvas.get_tk_widget().pack()

    def get_ratings(self, title):
        ratings = database.get_book_ratings(title)
        list_ratings = []
        #list_ratings = np.array([])
        if ratings is not None:
            for rating in ratings:
                list_ratings.append(rating[0])
                #np.append(list_ratings, rating[0])
            #values, counts = np.unique(list_ratings, return_counts=True)
            #self.counts = np.concatenate((self.counts, counts))
            sum1 = sum2 = sum3 = sum4 = sum5 = 0
            for i in list_ratings:
                match i:
                    case 1:
                        sum1 = sum1 + 1
                    case 2:
                        sum2 = sum2 + 1
                    case 3:
                        sum3 = sum3 + 1
                    case 4:
                        sum4 = sum4 + 1
                    case 5:
                        sum5 = sum5 + 1
            self.book_ratings[0] = sum1
            self.book_ratings[1] = sum2
            self.book_ratings[2] = sum3
            self.book_ratings[3] = sum4
            self.book_ratings[4] = sum5

    def plot_ratings(self):
        #fig = Figure(figsize=(2.5, 1.5))
        #ax = fig.add_subplot()
        fig, ax = plt.subplots(figsize=(2.5, 1.5))
        ax.bar(['1', '2', '3','4','5'], self.book_ratings)
        ax.set_yticks(self.book_ratings)
        ax.set_title("Book Ratings")
        fig.tight_layout()
        return fig
