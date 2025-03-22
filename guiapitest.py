from tkinter import *
import requests
from tkinter import filedialog
from PIL import Image, ImageTk
import sqlite3

url = 'https://www.googleapis.com/books/v1/volumes?q='
fields = '&fields=items(volumeInfo(title,authors,publisher,publishedDate,description,imageLinks,categories))'

def info_screen(master):
    master.title('Info Window')
    #login_signup_frame.destroy()
    info_frame = Frame(master)
    info_frame.pack()
    info_frame.columnconfigure(0, weight=1)
    info_frame.columnconfigure(1, weight=1)
    info_frame.columnconfigure(2, weight=2)
    info_frame.columnconfigure(3, weight=1)
    title_label = Label(info_frame, text='Title:')
    title_label.grid(row=0, column=1)
    title_entry = Entry(info_frame)
    title_entry.grid(row=0, column=2)
    author_label = Label(info_frame, text='Author:')
    author_label.grid(row=1, column=1)
    author_entry = Entry(info_frame)
    author_entry.grid(row=1, column=2)
    publisher_label = Label(info_frame, text='Publisher:')
    publisher_label.grid(row=2, column=1)
    publisher_entry = Entry(info_frame)
    publisher_entry.grid(row=2, column=2)
    year_published_label = Label(info_frame, text='Year published:')
    year_published_label.grid(row=3, column=1)
    year_published_entry = Entry(info_frame)
    year_published_entry.grid(row=3, column=2)
    image_label = Label(info_frame)
    image_label.grid(row=0, column=0, rowspan=3)
    add_image_button = Button(info_frame, text='Add Image', command=lambda: file_browser(image_label))
    add_image_button.grid(row=4, column=0)
    search_button = Button(info_frame, text='Search', command=lambda: show_data(info_frame, image_label, title_entry.get(), author_entry, publisher_entry, year_published_entry))
    search_button.grid(row=0, column=3)
    enter_data_button = Button(info_frame, text='Add', command=lambda: enter_data(title_entry.get(), author_entry.get(), publisher_entry.get(), year_published_entry.get()))
    enter_data_button.grid(row=3, column=3)

def show_data(info_frame_data, image_label_data, title_data, author_entry_data, publisher_entry_data, year_published_entry_data):
    thumbnail , author, publisher, published_date = get_data(title_data)
    img = Image.open(requests.get(thumbnail, stream=True).raw)
    img.thumbnail((128.0, 128.0), Image.Resampling.LANCZOS)
    photo_image = ImageTk.PhotoImage(img)
    image_label_data.config(image=photo_image)
    image_label_data.image = photo_image
    author_entry_data.delete(0, 'end')
    author_entry_data.insert(0, author)
    publisher_entry_data.delete(0, 'end')
    publisher_entry_data.insert(0, publisher)
    year_published_entry_data.delete(0, 'end')
    year_published_entry_data.insert(0, published_date)

def get_data(title_data):
    full_url = url + title_data + fields
    response = requests.get(full_url)
    if response.status_code == 200:
        book_data = response.json()
        thumbnail = book_data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
        author = book_data["items"][0]["volumeInfo"]["authors"][0]
        publisher = book_data["items"][0]["volumeInfo"]["publisher"]
        published_date = book_data["items"][0]["volumeInfo"]["publishedDate"]
        return thumbnail, author, publisher, published_date
    else:
        print("error")

def file_browser(image_label_data):
    fn = filedialog.askopenfilename(initialdir='/', title='Select a file')
    img = Image.open(fn)
    # width = img.width
    # height = img.height
    # ratio = min(128 / width, 256 / height)
    # new_size = (round(width * ratio), round(height * ratio))
    # new_image = img.resize(new_size, Image.Resampling.LANCZOS)
    img.thumbnail((128.0, 128.0), Image.Resampling.LANCZOS)
    photo_image = ImageTk.PhotoImage(img)        #new_image
    image_label_data.config(image=photo_image)
    image_label_data.image = photo_image

def create_database():
    c.execute('''CREATE TABLE users
               (username text,
               password text)''')
    c.execute('''CREATE TABLE books
               (title text,
               author text,
               publisher text,
               year published integer)''')
    c.execute('''CREATE TABLE ratings
               (number real,
               comment text)''')


def enter_data(title_data, author_data, publisher_data, published_date_data):
    c.execute("INSERT INTO books VALUES(?, ?, ?, ?)", (title_data, author_data, publisher_data, published_date_data))
    conn.commit()


root = Tk()
info_screen(root)
conn = sqlite3.connect('database.db')
c = conn.cursor()
#create_database()
root.mainloop()