import sqlite3
import requests

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
            release_year INTEGER,
            description TEXT,
            author TEXT NOT NULL,
            version TEXT,
            image BLOB
        )
    ''')

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

def insert_book(title, author, year, cover_url):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, year, cover_url) VALUES (?, ?, ?, ?)", (title, author, year, cover_url))
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
    if books:
        print("Βρέθηκαν τα ακόλουθα βιβλία:")
        for book in books:
            print(f"ID: {book[0]}, Τίτλος: {book[1]}, Συγγραφέας: {book[2]}, Έτος: {book[3]}, Εξώφυλλο: {book[4]}")
    else:
        print("Δεν βρέθηκε κάποιο βιβλίο με αυτόν τον τίτλο. Αναζήτηση στο Google Books API...")
        fetch_book_from_google_books(title)
        return books


if __name__ == "__main__":
    create_database()
    print("Η βάση δεδομένων δημιουργήθηκε επιτυχώς!")
    
    # Δοκιμαστική εισαγωγή χρήστη και βιβλίου
    insert_user("user1", "password123")
    insert_book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "https://example.com/gatsby.jpg")
    
    # Δοκιμαστική σύνδεση χρήστη
    login_user("user1", "password123")
    
    # Δοκιμαστική αναζήτηση βιβλίου
    search_books("Harry Potter")
