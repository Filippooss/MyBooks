import sqlite3
from api import Book

def create_database():
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()

    # 1) Δημιουργία πίνακα χρηστών (users)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')

    # 2) Δημιουργία πίνακα βιβλίων (books)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            author TEXT NOT NULL,
            version TEXT,
            image BLOB,
            release_year INTEGER,
            publisher TEXT
        )
    ''')

    # 3) Δημιουργία πίνακα βαθμολογιών (ratings)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER CHECK(value BETWEEN 1 AND 5),
            comment TEXT,
            username TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')

    # 4) Δημιουργία πίνακα συσχέτισης βιβλίων-βαθμολογιών (books_ratings)
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS books_ratings (
            book_id INTEGER,
            rating_id INTEGER,
            PRIMARY KEY (book_id, rating_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (rating_id) REFERENCES ratings(rating_id)
        )
    ''')

    # 5) Δημιουργία πίνακα συσχέτισης χρηστών-βιβλίων (user_book)
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

def insert_book(book_model: Book, username: str):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()

    # Εισαγωγή βιβλίου
    cursor.execute("""
        INSERT INTO books (title, description, author, version, image, release_year, publisher) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        book_model.title,
        book_model.description,
        book_model.author,
        book_model.version,
        book_model.image_raw,
        book_model.release_year,
        book_model.publisher
    ))
    book_id = cursor.lastrowid

    # Εύρεση user_id από το username
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_row = cursor.fetchone()
    if user_row:
        user_id = user_row[0]
        # Συσχέτιση με τον πίνακα user_book
        cursor.execute("INSERT INTO user_book (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        conn.commit()
        print("Το βιβλίο προστέθηκε επιτυχώς και συνδέθηκε με τον χρήστη!")
    else:
        print("Ο χρήστης δεν βρέθηκε. Δεν έγινε συσχέτιση βιβλίου.")

    conn.close()

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

def search_books(title: str, username: str):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_row = cursor.fetchone()
    if not user_row:
        print("Ο χρήστης δεν βρέθηκε.")
        conn.close()
        return []

    user_id = user_row[0]
    cursor.execute("""
        SELECT b.* FROM books b
        JOIN user_book ub ON b.book_id = ub.book_id
        WHERE ub.user_id = ? AND b.title LIKE ?
    """, (user_id, '%' + title + '%'))

    books = cursor.fetchall()
    conn.close()

    book_models = []
    if books:
        print("Βρέθηκαν τα ακόλουθα βιβλία:")
        for book in books:
            book_model = Book(
                id=book[0],
                title=book[1],
                description=book[2],
                author=book[3],
                version=book[4],
                image_raw=book[5],
                release_year=book[6],
                publisher=book[7]
            )
            book_models.append(book_model)
            print(f"ID: {book[0]}, Τίτλος: {book[1]}, Συγγραφέας: {book[3]}, Έτος: {book[6]}")
        return book_models
    else:
        print("Δεν βρέθηκε κάποιο βιβλίο.")
        return []

def get_books(username: str, page=1, books_per_page=10):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_row = cursor.fetchone()
    if not user_row:
        print("Ο χρήστης δεν βρέθηκε.")
        conn.close()
        return []

    user_id = user_row[0]
    offset = (page - 1) * books_per_page
    cursor.execute("""
        SELECT b.* FROM books b
        JOIN user_book ub ON b.book_id = ub.book_id
        WHERE ub.user_id = ?
        LIMIT ? OFFSET ?
    """, (user_id, books_per_page, offset))

    books = cursor.fetchall()
    conn.close()

    book_models = []
    if books:
        print(f"Σελίδα {page} - Βιβλία:")
        for book in books:
            book_model = Book(
                id=book[0],
                title=book[1],
                description=book[2],
                author=book[3],
                version=book[4],
                image_raw=book[5],
                release_year=book[6],
                publisher=book[7]
            )
            book_models.append(book_model)
            print(f"ID: {book[0]}, Τίτλος: {book[1]}, Συγγραφέας: {book[3]}, Έτος: {book[6]}")
        return book_models
    else:
        print(f"Δεν υπάρχουν βιβλία στη σελίδα {page}.")
        return []

def add_rating(username, book_id, value, comment):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO ratings (value, comment, username) VALUES (?, ?, ?)", (value, comment, username))
    rating_id = cursor.lastrowid

    cursor.execute("INSERT INTO books_ratings (book_id, rating_id) VALUES (?, ?)", (book_id, rating_id))

    conn.commit()
    conn.close()
    print("Η βαθμολογία προστέθηκε επιτυχώς!")

def get_book_ratings(book_title):
    conn = sqlite3.connect("mybooks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT book_id FROM books WHERE title = ?", (book_title,))
    result = cursor.fetchone()
    if not result:
        print("Δεν βρέθηκε βιβλίο με αυτόν τον τίτλο.")
        conn.close()
        return []

    book_id = result[0]
    cursor.execute("""
        SELECT r.value, r.comment, r.username
        FROM ratings r
        JOIN books_ratings br ON r.rating_id = br.rating_id
        WHERE br.book_id = ?
    """, (book_id,))
    ratings = cursor.fetchall()
    conn.close()

    if ratings:
        print(f"Βαθμολογίες για το βιβλίο: {book_title}")
        for r in ratings:
            print(f"Βαθμός: {r[0]}, Σχόλιο: {r[1]}, Χρήστης: {r[2]}")
    else:
        print("Δεν υπάρχουν βαθμολογίες για αυτό το βιβλίο.")

    return ratings  # Επιστροφή της λίστας


if __name__ == "__main__":
    create_database()
    insert_user("user1", "password123")
    login_user("user1", "password123")