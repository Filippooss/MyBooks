from csv import Error
import sqlite3
from Models.book_model import Book
from Models.rating_model import Rating


def create_database():
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()

            # 1) Users table creation (users)
            _ = cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """
            )

            # 2) Books table creation (books)
            _ = cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publisher TEXT,
                    release_year INTEGER,
                    description TEXT,
                    image BLOB
                )
            """
            )

            # 3) Ratings table creation (ratings)
            _ = cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ratings (
                    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value INTEGER CHECK(value BETWEEN 1 AND 5),
                    comment TEXT,
                    username TEXT NOT NULL,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            """
            )

            # 4) Books_ratings table creation (books_ratings)
            _ = cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS books_ratings (
                    book_id INTEGER,
                    rating_id INTEGER,
                    PRIMARY KEY (book_id, rating_id),
                    FOREIGN KEY (book_id) REFERENCES books(book_id),
                    FOREIGN KEY (rating_id) REFERENCES ratings(rating_id)
                )
            """
            )

            # 5) User_book table creation (user_book)
            _ = cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_book (
                    user_id INTEGER,
                    book_id INTEGER,
                    PRIMARY KEY (user_id, book_id),
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            """
            )

            print("Database created successful!")
    except Exception as e:
        print("Error while creating tables: ", e)


def insert_user(username: str, password: str):
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()
            _ = cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            print("User added successful!")
    except sqlite3.IntegrityError:
        print("User already exists!")


def insert_book(book_model: Book, username: str) -> bool:
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()

            # Insert Book
            _ = cursor.execute(
                """
                INSERT INTO books (title, description, author, image, release_year, publisher)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    book_model.title,
                    book_model.description,
                    book_model.author,
                    book_model.image_raw,
                    book_model.release_year,
                    book_model.publisher,
                ),
            )
            book_id = cursor.lastrowid

            # Find user_id
            _ = cursor.execute(
                "SELECT user_id FROM users WHERE username = ?", (username,)
            )
            user_row = cursor.fetchone()

            if not user_row:
                raise ValueError("User not found")

            user_id = user_row[0]
            # Link user with book
            _ = cursor.execute(
                "INSERT INTO user_book (user_id, book_id) VALUES (?, ?)",
                (user_id, book_id),
            )
            print("Book added successful!")
            return True
    except Exception as e:
        print("Error while inserting new book:", e)
        return False


def login_user(username: str, password: str) -> bool:
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()
            _ = cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password),
            )
            user = cursor.fetchone()
            if user:
                print("Login successful!", username)
                return True
            else:
                raise Error("Wrong username or password!")
    except Exception as e:
        print("Error while validating user:", e)
        return False


def search_books(title: str, username: str) -> list[Book]:
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()

            _ = cursor.execute(
                "SELECT user_id FROM users WHERE username = ?", (username,)
            )
            user_row = cursor.fetchone()
            if not user_row:
                raise Error("User not found")

            user_id = user_row[0]
            _ = cursor.execute(
                """
                SELECT b.* FROM books b
                JOIN user_book ub ON b.book_id = ub.book_id
                WHERE ub.user_id = ? AND b.title LIKE ?
                """,
                (user_id, "%" + title + "%"),
            )

            rows: list[tuple[int, str, str, str, int, str, bytes]] = cursor.fetchall()
            if not rows:
                raise Error("No books found")

            book_models: list[Book] = [
                Book(
                    id=r[0],
                    title=r[1],
                    author=r[2],
                    publisher=r[3],
                    release_year=r[4],
                    description=r[5],
                    image_raw=r[6],
                )
                for r in rows
            ]

            return book_models
    except Exception as e:
        print("Error while searching a book: ", e)
        return []


def get_books(username: str, page: int = 1, books_per_page=10) -> list[Book]:
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()

            _ = cursor.execute(
                "SELECT user_id FROM users WHERE username = ?", (username,)
            )
            user_row = cursor.fetchone()
            if not user_row:
                raise Error("User not found.")

            user_id = user_row[0]
            offset = (page - 1) * books_per_page
            _ = cursor.execute(
                """
                SELECT b.* FROM books b
                JOIN user_book ub ON b.book_id = ub.book_id
                WHERE ub.user_id = ?
                LIMIT ? OFFSET ?
            """,
                (user_id, books_per_page, offset),
            )

            rows: list[tuple[int, str, str, str, int, str, bytes]] = cursor.fetchall()
            if not rows:
                raise Error(f"No books in the page {page}.")

            book_models: list[Book] = [
                Book(
                    id=r[0],
                    title=r[1],
                    author=r[2],
                    publisher=r[3],
                    release_year=r[4],
                    description=r[5],
                    image_raw=r[6],
                )
                for r in rows
            ]
            return book_models

    except Exception as e:
        print("Error while getting books: ", e)
        return []


def add_rating(username: str, book_id: str, value: int, comment: str):
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()

            _ = cursor.execute(
                "INSERT INTO ratings (value, comment, username) VALUES (?, ?, ?)",
                (value, comment, username),
            )
            rating_id = cursor.lastrowid

            _ = cursor.execute(
                "INSERT INTO books_ratings (book_id, rating_id) VALUES (?, ?)",
                (book_id, rating_id),
            )
            print("Rating added successful")
    except Exception as e:
        print("Error while adding rating: ", e)


def get_book_ratings(book_title: str) -> list[Rating]:
    try:
        with sqlite3.connect("mybooks.db") as conn:
            cursor = conn.cursor()

            _ = cursor.execute(
                "SELECT book_id FROM books WHERE title = ?", (book_title,)
            )
            result = cursor.fetchone()
            if not result:
                raise Error("No book with this title")

            book_id = result[0]
            _ = cursor.execute(
                """
                SELECT r.value, r.comment, r.username
                FROM ratings r
                JOIN books_ratings br ON r.rating_id = br.rating_id
                WHERE br.book_id = ?
            """,
                (book_id,),
            )
            rows: list[tuple[int, int, str, str]] = cursor.fetchall()
            if not rows:
                raise Error("No ratings found.")

            ratings: list[Rating] = [Rating(r[0], r[1], r[2], r[3]) for r in rows]
            print(f"Ratings for book: {book_title}")
            for r in ratings:
                print(f"Value: {r.value}, Comment: {r.comment}, User: {r.username}")

            return ratings
    except Exception as e:
        print("Error while fetching book ratings: ", e)
        return []


if __name__ == "__main__":
    create_database()
    # insert_user("user1", "password123")
    # login_user("user1", "password123")
