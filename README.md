# MyBooks

<<<<<<< HEAD
**My Books** is a desktop application built with Python that allows users to manage their personal book collection.

The application follows the **MVC (Model–View–Controller)** architecture and uses a local database to store user accounts, books and user ratings.

Users can create an account, log in, and manage their own library by adding, viewing, and deleting books.

## 🧱 Architecture

**The project is structured using the MVC pattern:**  
Model → Handles database and data logic  
View → Graphical User Interface built with Tkinter  
Controller → Connects the UI with the data and handles user actions

## ✨ Features

**👤 User Authentication**  
• Register a new account  
• Login with existing credentials

**📚 Book Management**  
• Add a new book  
• View all saved books  
• Delete a book  
• Search books online

## 🗄️ Database

**The app uses a local database to store:**  
• Users (user_id, username, password)  
• Books (book_id, title, description, author, image, release_year, publisher)  
• Ratings (rating_id, value, comment, username)  
• User Book (user_id, book_id)  
• Books Ratings (book_id, rating_id)

## 🖥️ User Interface

The GUI is implemented using Tkinter, providing:
• Login & Register forms  
• Book list display  
• Book entry form

## ⚙️ Technologies Used

• Python  
• MVC Architecture  
• Tkinter  
• SQLite  
• Goggle Book API

## 🚀 How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/Filippooss/MyBooks.git
```

2. Navigate into the project folder:

```bash
cd MyBooks
```

3. Run the application:

```bash
python app.py
```

## 👨‍🎓 Author

Created as a university project for a course assignment

## 📜 License

This project is for educational purposes.
=======
MyBooks is a python based, user friendly program, that allows the user to search, save and manage books that they desire. This program can be used offline as well as online. This project was made by computer science students for the final assignment.
>>>>>>> 00e041434c91e9640af688e75c99041fe4a67d07
