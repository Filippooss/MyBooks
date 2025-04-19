import sqlite3
import requests

def create_database():
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()
    
    # Δημιουργία πίνακα χρηστών
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Δημιουργία πίνακα βιβλίων
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            cover_url TEXT
        )
    ''')
    
    # Δημιουργία πίνακα βαθμολογιών και σχολίων
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            rating INTEGER CHECK(rating BETWEEN 1 AND 5),
            comment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
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

def fetch_book_from_google_books(title):
    url = f"https://www.googleapis.com/books/v1/volumes?q={title}&maxResults=1&printType=books&projection=lite"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            book_info = data["items"][0]["volumeInfo"]
            book_title = book_info.get("title", "Άγνωστο")
            book_author = ", ".join(book_info.get("authors", ["Άγνωστος"]))
            book_year = book_info.get("publishedDate", "Άγνωστο")[:4]
            book_cover = book_info.get("imageLinks", {}).get("thumbnail", "")
            
            print(f"Βιβλίο από Google Books:")
            print(f"Τίτλος: {book_title}")
            print(f"Συγγραφέας: {book_author}")
            print(f"Έτος: {book_year}")
            print(f"Εξώφυλλο: {book_cover}")
            
            insert_book(book_title, book_author, book_year, book_cover)
        else:
            print("Δεν βρέθηκε βιβλίο στο Google Books API.")
    else:
        print("Σφάλμα κατά την επικοινωνία με το Google Books API.")

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
