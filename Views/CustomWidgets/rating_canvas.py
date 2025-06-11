import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
#import numpy as np

import database

class RatingCanvas(tk.Frame):
    def __init__(self, master, title):
        super().__init__(master=master)
        #self.counts = np.array([], dtype=int)
        self.book_ratings = [0,0,0,0,0]     #Αρχικοποιώντας σε 0 άν δεν υπάρχουν αξιολογήσεις θα δείχνει κενό γράφημα
        self.get_ratings(title)

        canvas = FigureCanvasTkAgg(self.plot_ratings(),master=self)
        canvas.draw()

        canvas.get_tk_widget().pack()

    def get_ratings(self, title):
        ratings = database.get_book_ratings(title)      #Η ratings είναι λίστα από πλειάδες της μορφής (rating, comment, username)
        list_ratings = []
        #list_ratings = np.array([])
        if ratings is not None:
            for entry in ratings:       #Για κάθε μία πλειάδα
                list_ratings.append(entry[0])       #Προσθέτουμε στη λίστα μόνο την αξιολόγηση
                #np.append(list_ratings, entry[0])
            #values, counts = np.unique(list_ratings, return_counts=True)
            #self.counts = np.concatenate((self.counts, counts))
            #Μετράμε πόσες φορές εμφανίζονται οι ξεχωριστοί αριθμοί 1,2,3,4,5
            sum1 = sum2 = sum3 = sum4 = sum5 = 0
            for i in list_ratings:      #Για κάθε μία αξιολόγηση
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
            #Αλλάζουμε τα στοιχεία της book_ratings (αρχικά 0)
            self.book_ratings[0] = sum1
            self.book_ratings[1] = sum2
            self.book_ratings[2] = sum3
            self.book_ratings[3] = sum4
            self.book_ratings[4] = sum5

    def plot_ratings(self):
        #fig = Figure(figsize=(2.5, 1.5))
        #ax = fig.add_subplot()
        fig, ax = plt.subplots(figsize=(2.5, 1.5))      #Σχέδιο και άξονες σε ένα plot
        ax.bar(['1', '2', '3','4','5'], self.book_ratings)      #Ετικέτες του χ οι τιμές 1-5, τιμές του y οι τιμές της book_ratings
        ax.set_yticks(self.book_ratings)        #Ετικέτες του y οι τιμές της book_ratings
        ax.set_title("Book Ratings")
        fig.tight_layout()      #Επειδή το γράφημα είναι μικρό το tight_layout() βοηθάει
        return fig
