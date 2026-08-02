from abc import ABC, abstractmethod
import csv
import os

class Library(ABC):

    def __init__(self, title, book_id, author):
        self.__title = title
        self.__book_id = book_id
        self.__author = author

    def get_title(self):
        return self.__title

    def get_book_id(self):
        return self.__book_id

    def get_author(self):
        return self.__author

    def set_title(self, title):
        self.__title = title

    def set_author(self, author):
        self.__author = author

    @abstractmethod
    def display_details(self):
        pass

class Book(Library):

    def __init__(self, title, book_id, author, status = 'Available'):
        super().__init__(title, book_id, author)
        self.__status = status

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def display_details(self):
        print("\n------------------------")
        print(f"Book Title: {self.get_title()}")
        print(f"Book ID   : {self.get_book_id()}")
        print(f"Author    : {self.get_author()}")
        print(f"Status    : {self.get_status()}")
        print("\n------------------------")

class LibraryManagementSystem:

    file_name = 'books.csv'

    def __init__(self):
        self.books = []
        self.load_records()

    def add_book(self):
        try:
            book_id = input("Enter the book ID: ")

            if self.search_book(book_id, show=False):
                print("Book ID already exists")
                return

            title = input("Enter the book title: ")
            author = input("Enter the book author: ")
            book = Book(title, book_id, author)

            self.books.append(book)

            print("Book added successfully!")
            
        except Exception as e:
            print("Error adding book", e)

    def search_book(self, book_id=None, show=True):
        if book_id is None:
            book_id = input("Enter the book ID:")

        for book in self.books:
            if book.get_book_id() == book_id:
                if show:
                    print("\nBook found: ")
                    book.display_details()
                return book

        if show:
            print("\nBook not found")

        return None

    def issue_book(self):
        book_id = input("Enter the book ID: ")
        book = self.search_book(book_id, show=False)

        if book:
            if book.get_status() == "Issued":
                print("\nBook Already Issued")

            else:
                book.set_status("Issued")
                print("\nBook has been Issued Successfully!")

        else:
            print("Book not found")

    def return_book(self):
        book_id = input("Enter book ID to Return: ")
        book = self.search_book(book_id, show=False)

        if book:
            if book.get_status() == "Available":
                print("\nBook is already available")

            else:
                book.set_status("Available")
                print("Book Returned Successfully!")
        else:
            print("Book not found")

    def display_available_books(self):
        available = False

        for book in self.books:
            if book.get_status() == "Available":
                book.display_details()
                available = True

        if not available:
            print("No books are available.")

    def save_records(self):

        try:
            with open(self.file_name, "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow(["Book Title", "Book ID", "Book Author", "Status"])

                for book in self.books:
                    
                    writer.writerow([
                        book.get_title(),
                        book.get_book_id(),
                        book.get_author(),
                        book.get_status()
                    ])
            print("Records saved Successfully!")

            print("File saved at:")
            print(os.path.abspath(self.file_name))

        except IOError:
            print("Error saving records")

    def load_records(self):
        if not os.path.exists(self.file_name):
            return

        try:
            with open(self.file_name, "r") as file:
                reader = csv.reader(file)

                next(reader)

                for row in reader:

                    book = Book(
                        row[0],
                        int(row[1]),
                        row[2],
                        row[3]
                    )

                    self.books.append(book)
        except (IOError, ValueError):
            print("Error loading records.")

    def menu(self):
        
        while True:

            print("\n=======Library Management System=======")
            print("1. Add Book")
            print("2. Search Book")
            print("3. Issue Book")
            print("4. Return Book")
            print("5. Display Available Books")
            print("6. Save Records")
            print("7. Exit")
            
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_book()

            elif choice == "2":
                self.search_book()

            elif choice == "3":
                self.issue_book()

            elif choice == "4":
                self.return_book()

            elif choice == "5":
                self.display_available_books()

            elif choice == "6":
                self.save_records()

            elif choice == "7":
                self.load_records()
                print("Thank you!")
                break

            else:
                print("Invalid choice.")

if __name__ == "__main__":
    system = LibraryManagementSystem()
    system.menu()
