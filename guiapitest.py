from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen
from urllib import request
from tkinter import filedialog
import json


class Application:
    def __init__(self, master):
        master.title('Info Window')
        # login_signup_frame.destroy()
        self.info_frame = Frame(master)
        self.info_frame.pack()
        self.info_frame.columnconfigure(0, weight=1)
        self.info_frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(2, weight=2)
        self.info_frame.columnconfigure(3, weight=1)
        self.title_label = Label(self.info_frame, text='Title:')
        self.title_label.grid(row=0, column=1)
        self.title_entry = Entry(self.info_frame)
        self.title_entry.grid(row=0, column=2)
        self.author_label = Label(self.info_frame, text='Author:')
        self.author_label.grid(row=1, column=1)
        self.author_entry = Entry(self.info_frame)
        self.author_entry.grid(row=1, column=2)
        self.publisher_label = Label(self.info_frame, text='Publisher:')
        self.publisher_label.grid(row=2, column=1)
        self.publisher_entry = Entry(self.info_frame)
        self.publisher_entry.grid(row=2, column=2)
        self.year_published_label = Label(self.info_frame, text='Year published:')
        self.year_published_label.grid(row=3, column=1)
        self.year_published_entry = Entry(self.info_frame)
        self.year_published_entry.grid(row=3, column=2)
        self.image_label = Label(self.info_frame)
        self.image_label.grid(row=0, column=0, rowspan=3)
        self.add_image_button = Button(self.info_frame, text='Add Image', command=self.file_browser)
        self.add_image_button.grid(row=4, column=0)
        self.search_button = Button(self.info_frame, text='Search',
                               command=lambda: self.search_widget(master))
        self.search_button.grid(row=0, column=3)
        self.enter_data_button = Button(self.info_frame, text='Add')
        self.enter_data_button.grid(row=3, column=3)

    def search_widget(self, master_data):
        self.new_win = Toplevel(master_data)
        self.search_frame = Frame(self.new_win)
        self.search_frame.pack()
        book_info_frames = []
        for i in range(4):
            b_i_f = self.create_frame(i)
            book_info_frames.append(b_i_f)
        for i in range(4):
            book_info_frames[i].grid(row=i)

    def create_frame(self, iter_num):
        book_info_frame = Frame(self.search_frame)
        book_info_frame.grid(row=0, column=0)
        title_data, author_data, publisher_data, published_date_data, thumbnail_data = self.get_info(iter_num)
        img = Image.open(urlopen(thumbnail_data))
        img.thumbnail((128.0, 128.0), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(img)
        book_image_label = Label(book_info_frame)   #image=photo_image
        book_image_label['image'] = photo_image
        book_image_label.grid(row=0, column=0, rowspan=3)
        book_image_label.image = photo_image
        book_title_label = Label(book_info_frame, text=title_data)
        book_title_label.grid(row=0, column=1)
        book_author_label = Label(book_info_frame, text=author_data)
        book_author_label.grid(row=1, column=1)
        book_publisher_label = Label(book_info_frame, text=publisher_data)
        book_publisher_label.grid(row=2, column=1)
        book_published_date_label = Label(book_info_frame, text=published_date_data)
        book_published_date_label.grid(row=3, column=1)
        add_button = Button(book_info_frame, text='Add book', command=lambda :self.show_data(iter_num))
        add_button.grid(row=3, column=2)
        return book_info_frame


    def show_data(self, num):
        self.new_win.destroy()
        title, author, publisher, published_date, thumbnail = self.get_info(num)
        img = Image.open(urlopen(thumbnail))
        img.thumbnail((128.0, 128.0), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(img)
        #self.image_label.config(image=photo_image)
        self.image_label['image'] = photo_image
        self.image_label.image = photo_image
        self.author_entry.delete(0, 'end')
        self.author_entry.insert(0, author)
        self.publisher_entry.delete(0, 'end')
        self.publisher_entry.insert(0, publisher)
        self.year_published_entry.delete(0, 'end')
        self.year_published_entry.insert(0, published_date)

    def file_browser(self):
        fn = filedialog.askopenfilename(initialdir='/', title='Select a file')
        img = Image.open(fn)
        # width = img.width
        # height = img.height
        # ratio = min(128 / width, 256 / height)
        # new_size = (round(width * ratio), round(height * ratio))
        # new_image = img.resize(new_size, Image.Resampling.LANCZOS)
        img.thumbnail((256.0, 128.0), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(img)  # new_image
        #self.image_label.config(image=photo_image)
        self.image_label['image'] = photo_image
        self.image_label.image = photo_image

    def get_info(self, number):
        url = 'https://www.googleapis.com/books/v1/volumes?q='
        max_results = '&maxResults=5'
        fields = '&fields=items(volumeInfo(title,authors,publisher,publishedDate,description,categories,imageLinks))'
        full_url = url + self.title_entry.get().replace(" ", "%20") + max_results + fields
        response = request.urlopen(full_url)
        if response.code == 200:
            data = response.read()
            book_data = data.decode('Utf-8')
            data_needed = json.loads(book_data)
            if "items" in data_needed:
                if "title" in data_needed["items"][number]["volumeInfo"]:
                    title = data_needed["items"][number]["volumeInfo"]["title"]
                else:
                    title = ''
                if "imageLinks" in data_needed["items"][number]["volumeInfo"]:
                    thumbnail = data_needed["items"][number]["volumeInfo"]["imageLinks"]["thumbnail"]
                else:
                    thumbnail = ''
                if "authors" in data_needed["items"][number]["volumeInfo"]:
                    author = data_needed["items"][number]["volumeInfo"]["authors"][0]
                else:
                    author = ''
                if "publisher" in data_needed["items"][number]["volumeInfo"]:
                    publisher = data_needed["items"][number]["volumeInfo"]["publisher"]
                else:
                    publisher = ''
                if "publishedDate" in data_needed["items"][number]["volumeInfo"]:
                    published_date = data_needed["items"][number]["volumeInfo"]["publishedDate"]
                else:
                    published_date = ''
                return title, author, publisher, published_date, thumbnail
            else:
                print('not found')
        else:
            print('error')

class Api:
    def __init__(self):
        pass

    def get_info(self, title_data):
        url = 'https://www.googleapis.com/books/v1/volumes?q='
        max_results = '&maxResults=10'
        fields = '&fields=items(volumeInfo(title,authors,publisher,publishedDate,description,categories,imageLinks))'
        full_url = url + title_data.replace(" ", "%20") + max_results + fields
        response = request.urlopen(full_url)
        if response.code == 200:
            data = response.read()
            book_data = data.decode('Utf-8')
            data_needed = json.loads(book_data)
            results_list = []
            results_dict = {}
            if "items" in data_needed:
                for number in range(len(data_needed["items"])):
                    if "title" in data_needed["items"][number]["volumeInfo"]:
                        title = data_needed["items"][number]["volumeInfo"]["title"]
                    else:
                        title = ''
                    if "imageLinks" in data_needed["items"][number]["volumeInfo"]:
                        thumbnail = data_needed["items"][number]["volumeInfo"]["imageLinks"]["thumbnail"]
                    else:
                        thumbnail = ''
                    if "authors" in data_needed["items"][number]["volumeInfo"]:
                        author = data_needed["items"][number]["volumeInfo"]["authors"][0]
                    else:
                        author = ''
                    if "publisher" in data_needed["items"][number]["volumeInfo"]:
                        publisher = data_needed["items"][number]["volumeInfo"]["publisher"]
                    else:
                        publisher = ''
                    if "publishedDate" in data_needed["items"][number]["volumeInfo"]:
                        published_date = data_needed["items"][number]["volumeInfo"]["publishedDate"]
                    else:
                        published_date = ''
                    if "description" in data_needed["items"][number]["volumeInfo"]:
                        description = data_needed["items"][number]["volumeInfo"]["description"]
                    else:
                        description = ''
                    results_dict = {"Τίτλος": title, "Συγγραφέας": author, "Εκδότης": publisher, "Έτος έκδοσης": published_date, "Εξώφυλλο": thumbnail, "Περιγραφή": description}
                    results_list.append(results_dict)
                return results_dict
            else:
                print('not found')
        else:
            print('error')


root = Tk()
application = Application(root)
root.mainloop()