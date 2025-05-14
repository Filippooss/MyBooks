from asyncio.windows_events import NULL
import sqlite3

import requests

from api import Book


def create_database():
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()

    # 1) Δημιουργία πίνακα χρηστών (User)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')

    # 2) Δημιουργία πίνακα βιβλίων (Books)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            author TEXT NOT NULL,
            version TEXT,
            image BLOB
        )
    ''')

    # ✅ Αν δεν υπάρχει η στήλη release_year, την προσθέτουμε
    cursor.execute("PRAGMA table_info(books)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'release_year' not in columns:
        cursor.execute("ALTER TABLE books ADD COLUMN release_year INTEGER")

    # 3) Δημιουργία πίνακα βαθμολογιών (Ratings)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER CHECK(value BETWEEN 1 AND 5),
            comment TEXT,
            username TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')

    # 4) Δημιουργία πίνακα συσχέτισης βιβλίων-βαθμολογιών (Books_Ratings)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS books_ratings (
            book_id INTEGER,
            rating_id INTEGER,
            PRIMARY KEY (book_id, rating_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (rating_id) REFERENCES ratings(rating_id)
        )
    ''')

    # 5) Δημιουργία πίνακα συσχέτισης χρηστών-βιβλίων (User_Book)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS user_book (
            user_id INTEGER,
            book_id INTEGER,
            PRIMARY KEY (user_id, book_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Η βάση δεδομένων δημιουργήθηκε επιτυχώς!")

def insert_user(username, password):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Ο χρήστης προστέθηκε επιτυχώς!")
    except sqlite3.IntegrityError:
        print("Το όνομα χρήστη υπάρχει ήδη!")
    conn.close()

def insert_book(book_model:Book):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, release_year, image) VALUES (?, ?, ?, ?)", (book_model.title, book_model.author, book_model.release_year, book_model.image_raw))
    conn.commit()
    conn.close()
    print("Το βιβλίο προστέθηκε επιτυχώς!")

def login_user(username, password):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Σύνδεση επιτυχής! Καλώς ήρθες,", username)
        return True
    else:
        print("Λάθος όνομα χρήστη ή κωδικός!")
        return False

def search_books(title):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    books = cursor.fetchall()
    conn.close()
    book_models=[]
    if books:
        print("Βρέθηκαν τα ακόλουθα βιβλία:")
        for book in books:
            book_model = Book(id=book[0], 
                              title= book[1], 
                              description=book[2], 
                              author= book[3], 
                              version=book[4], 
                              image_raw=book[5], 
                              release_year=book[6],
                              publisher=""
                              )
            book_models.append(book_model)
            print(f"ID: {book[0]}, Τίτλος: {book[1]}, Συγγραφέας: {book[3]}, Έτος: {book[6]}, Εξώφυλλο: {book[5]}")
        return book_models
    else:
        return list()
        print("Δεν βρέθηκε κάποιο βιβλίο με αυτόν τον τίτλο.")

def get_books(page=1, books_per_page=10):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()
    
    offset = (page - 1) * books_per_page
    cursor.execute("SELECT * FROM books LIMIT ? OFFSET ?", (books_per_page, offset))
    books = cursor.fetchall()
    conn.close()
    book_models=[]
    if books:
        print(f"Σελίδα {page} - Βιβλία:")
        for book in books:
            book_model = Book(id=book[0], 
                              title= book[1], 
                              description=book[2], 
                              author= book[3], 
                              version=book[4], 
                              image_raw=book[5], 
                              release_year=book[6],
                              publisher=""
                              )
            book_models.append(book_model)
            print(f"ID: {book[0]}, Τίτλος: {book[1]}, Συγγραφέας: {book[3]}, Έτος: {book[6]}, Εξώφυλλο: {book[5]}")
        return book_models
    else:
        print(f"Δεν υπάρχουν βιβλία στη σελίδα {page}.")
        return list()

# Εκκίνηση αν τρέχει ως κύριο πρόγραμμα
if __name__ == "__main__":
    create_database()
    
    # Εισαγωγή δοκιμαστικού χρήστη
    insert_user("user1", "password123")

    # Δοκιμαστική σύνδεση χρήστη
    login_user("user1", "password123")

    # Δοκιμαστική αναζήτηση και εμφάνιση βιβλίων
    search_books("Gatsby")
    get_books(page=1)