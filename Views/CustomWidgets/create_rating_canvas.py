import database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RatingCanvas:
    def __init__(self, master, title):
        self.book_ratings = []
        self.get_ratings(title)
        self.plot_ratings(master)

    def get_ratings(self, title):
        ratings = database.get_book_ratings(title)
        list_ratings = []
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
        self.book_ratings.append(sum1)
        self.book_ratings.append(sum2)
        self.book_ratings.append(sum3)
        self.book_ratings.append(sum4)
        self.book_ratings.append(sum5)

    def plot_ratings(self, master):
        fig, plot1 = plt.subplots(figsize=(2.5, 1))
        plot1.bar(['1', '2', '3','4','5'], self.book_ratings)
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack()