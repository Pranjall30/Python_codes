#Automated Library Management System

from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity
        self.checked_out_by = {}  # {user_id: checkout_date}

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.checked_out_books = []  # List of book IDs

class Library:
    def __init__(self):
        self.catalog = {}  # {book_id: Book}
        self.users = {}  # {user_id: User}

    def add_book(self, book_id, title, author, quantity):
        if book_id in self.catalog:
            print("Book ID already exists.")
        else:
            self.catalog[book_id] = Book(book_id, title, author, quantity)
            print(f"Book '{title}' added to catalog.")

    def remove_book(self, book_id):
        if book_id in self.catalog:
            del self.catalog[book_id]
            print("Book removed from catalog.")
        else:
            print("Book ID not found in catalog.")

    def display_catalog(self):
        print("\nCatalog:")
        for book_id, book in self.catalog.items():
            availability = "Available" if book.quantity > len(book.checked_out_by) else "Unavailable"
            print(f"ID: {book_id}, Title: {book.title}, Author: {book.author}, Availability: {availability}")

    def register_user(self, user_id, name):
        if user_id in self.users:
            print("User ID already exists.")
        else:
            self.users[user_id] = User(user_id, name)
            print(f"User '{name}' registered.")

    def checkout_book(self, user_id, book_id):
        if user_id not in self.users:
            print("User ID not found.")
            return
        if book_id not in self.catalog:
            print("Book ID not found.")
            return
        user = self.users[user_id]
        book = self.catalog[book_id]
        if len(user.checked_out_books) >= 3:
            print("User has reached the maximum limit of checked-out books.")
            return
        if user_id in book.checked_out_by:
            print("Book already checked out by this user.")
            return
        if book.quantity <= len(book.checked_out_by):
            print("Book not available for checkout.")
            return
        book.checked_out_by[user_id] = datetime.now()
        user.checked_out_books.append(book_id)
        print(f"Book '{book.title}' checked out by '{user.name}'. Due in 14 days.")

    def return_book(self, user_id, book_id):
        if user_id not in self.users:
            print("User ID not found.")
            return
        if book_id not in self.catalog:
            print("Book ID not found.")
            return
        user = self.users[user_id]
        book = self.catalog[book_id]
        if user_id not in book.checked_out_by:
            print("User hasn't checked out this book.")
            return
        checkout_date = book.checked_out_by.pop(user_id)
        user.checked_out_books.remove(book_id)
        return_date = datetime.now()
        days_overdue = (return_date - (checkout_date + timedelta(days=14))).days
        if days_overdue > 0:
            fine = days_overdue * 1
            print(f"Book '{book.title}' returned by '{user.name}' after due date. Fine: ${fine}.")
        else:
            print(f"Book '{book.title}' returned by '{user.name}'.")

    def list_overdue_books(self, user_id):
        if user_id not in self.users:
            print("User ID not found.")
            return
        user = self.users[user_id]
        overdue_books = []
        total_fine = 0
        for book_id in user.checked_out_books:
            book = self.catalog[book_id]
            checkout_date = book.checked_out_by[user_id]
            due_date = checkout_date + timedelta(days=14)
            if datetime.now() > due_date:
                days_overdue = (datetime.now() - due_date).days
                fine = days_overdue * 1
                total_fine += fine
                overdue_books.append((book.title, fine))
        if overdue_books:
            print("\nOverdue Books:")
            for title, fine in overdue_books:
                print(f"Title: {title}, Fine: ${fine}")
            print(f"Total Fine: ${total_fine}")
        else:
            print("No overdue books.")

    def extend_due_date(self, user_id, book_id):
        if user_id not in self.users:
            print("User ID not found.")
            return
        if book_id not in self.catalog:
            print("Book ID not found.")
            return
        user = self.users[user_id]
        book = self.catalog[book_id]
        if user_id not in book.checked_out_by:
            print("User hasn't checked out this book.")
            return
        checkout_date = book.checked_out_by[user_id]
        due_date = checkout_date + timedelta(days=14)
        if datetime.now() > due_date:
            print("Cannot extend due date after the book is overdue.")
            return
        if book_id in user.checked_out_books:
            print("Book already checked out by this user.")
            return
        book.checked_out_by[user_id] = datetime.now()
        user.checked_out_books.append(book_id)
        print(f"Due date extended for book '{book.title}' for user '{user.name}'.")

def main():
    library = Library()

    # Adding some initial books to the catalog
    library.add_book(1, "The White Tiger", "Aravind Adiga", 5)
    library.add_book(2, "Midnight's Children", "Salman Rushdie", 3)
    library.add_book(3, "The Guide", "R.K. Narayan", 4)

    # Registering some users
    library.register_user(101, "ekta")
    library.register_user(102, "isha")

    # Displaying the catalog
    library.display_catalog()

    # Checking out and returning books
    library.checkout_book(101, 1)
    library.checkout_book(102, 2)
    library.return_book(101, 1)
    library.return_book(102, 2)

    # Listing overdue books for a user
    library.checkout_book(101, 3)
    library.checkout_book(102, 3)
    library.list_overdue_books(101)

    # Extending due date for a book
    library.extend_due_date(101, 3)

if __name__ == "__main__":
    main()
