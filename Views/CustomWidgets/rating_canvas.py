import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import database


class RatingCanvas(tk.Frame):
    def __init__(self, master, title):
        super().__init__(master=master)
        self.book_ratings = [0,0,0,0,0]
        self.get_ratings(title)

        canvas = FigureCanvasTkAgg(self.plot_ratings(), master=master)
        canvas.draw()

        canvas.get_tk_widget().pack()

    def get_ratings(self, title):
        ratings = database.get_book_ratings(title)
        list_ratings = []
        if ratings is not None:
            for rating in ratings:
                list_ratings.append(rating[0])
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
        fig, plot1 = plt.subplots(figsize=(2.5, 1))
        plt.tight_layout()
        plot1.bar(['1', '2', '3','4','5'], self.book_ratings)
        return fig
