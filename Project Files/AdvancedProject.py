import tkinter as tk
from tkinter import messagebox, simpledialog
from abc import ABC, abstractmethod
import re
from datetime import datetime, timedelta


# Item class (The main Parent)
class Item(ABC):
    def __init__(self, title, author, price, rating):
        self._title = title
        self._author = author
        self._price = price
        self._rating = rating

    @abstractmethod
    def get_details(self):
        pass

    def update_details(self, new_title, new_author, new_price, new_rating):
        self._title = new_title
        self._author = new_author
        self._price = new_price
        self._rating = new_rating


# Book class
class Book(Item):
    def __init__(self, title, author, price, rating, isbn, genre, number_of_pages):
        super().__init__(title, author, price, rating)
        self._isbn = isbn
        self._genre = genre
        self._number_of_pages = number_of_pages

    def get_details(self):
        return f"Rating: {self._rating}\nISBN: {self._isbn}\nGenre: {self._genre}\nNumber of Pages: {self._number_of_pages}"


# Magazine class
class Magazine(Item):
    def __init__(self, title, price, rating, issue_number, publication_date, editor):
        super().__init__(title, "", price, rating)
        self._issue_number = issue_number
        self._publication_date = publication_date
        self._editor = editor

    def get_details(self):
        return f"Rating: {self._rating}\nIssue Number: {self._issue_number}\nPublication Date: {self._publication_date}\nEditor: {self._editor}"


# DVD class
class DVD(Item):
    def __init__(self, title, price, rating, director, duration, genre):
        super().__init__(title, "", price, rating)
        self._director = director
        self._duration = duration
        self._genre = genre

    def get_details(self):
        return f"Rating: {self._rating}\nDirector: {self._director}\nDuration: {self._duration}\nGenre: {self._genre}"


# All books:
books = [
    Book("The Great Gatsby", "F. Scott Fitzgerald", 12.99, "3.9/5", "978-0743273565", "Fiction", 180),
    Book("To Kill a Mockingbird", "Harper Lee", 10.50, "4.3/5", "978-0061120084", "Classic", 324),
    Book("1984", "George Orwell", 14.75, "4.5/5", "978-0451524935", "Dystopian", 328),
]

# All Magazines:
magazines = [
    Magazine("Scientific American", 11.44, "4.6/5 - Amazon", "Volume 325, Issue 2", "Monthly", "Laura Helmuth"),
    Magazine("The Economist", 13.48, "4.5/5 - Amazon", "Volume 435, Issue 9185", "Weekly", "Zanny Minton Beddoes"),
    Magazine("Nature", 12.86, "4.7/5 - Amazon", "Volume 594, Issue 7864", "Weekly", "Magdalena Skipper"),
]

# All DVDs:
dvds = [
    DVD("Inception", 8.99, "8.8/10 - IMDb", "Christopher Nolan", "2h 28m", "Thriller"),
    DVD("The Matrix", 9.75, "8.7/10 - IMDb", "Lana Wachowski", "2h 16m", "Science Fiction"),
    DVD("Pulp Fiction", 7.50, "8.9/10 - IMDb", "Quentin Tarantino", "2h 34m", "Crime"),
]

# empty cart to append items customer will buy
cart = []


def create_customer_gui():
    # Creating main window for customers:
    root1 = tk.Tk()
    root1.title("Quirk Byte Online Bookstore")
    image_path = "/home/huevvn/Documents/My Projects/Python Projects/My First Python Project/1.png"
    image_1 = tk.PhotoImage(file=image_path)
    root1.geometry("1400x840")
    background_label_0 = tk.Label(root1, image=image_1)
    background_label_0.place(x=0, y=0, relwidth=1, relheight=1)

    # if user pressed "Esc" button on keyboard
    def on_escape_1(event):
        root1.destroy()

    # Letting tk define Esc button as the event which run "on_escape" function to quit program
    root1.bind("<Escape>", on_escape_1)

    # Function to add item to cart
    def add_to_cart(item):
        cart.append(item)
        update_cart_button_text()
        messagebox.showinfo("Success", f"{item._title} added to cart.")

    # Function to update cart button text
    def update_cart_button_text():
        number_of_items = len(cart)
        button_cart.config(text=f"View Cart ({number_of_items})")

    # Function to display details
    def display_details(item):
        messagebox.showinfo("Details", item.get_details())

    # Function to get user data
    def get_user_data():
        try:
            email = simpledialog.askstring("User Data", "Enter your email:")
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Please enter a valid email address.")

            password = simpledialog.askstring("User Data", "Enter your password:")
            mobile_number = simpledialog.askstring("User Data", "Enter your mobile number (egy - 11 numbers):")
            if not re.match(r"^\d{11}$", mobile_number):
                raise ValueError("Please enter a valid 11-digit mobile number.")

            address = simpledialog.askstring("User Data", "Enter your address:")

            # Set expected date to be within 3 to 14 days
            expected_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

            return {
                "email": email,
                "password": password,
                "mobile_number": mobile_number,
                "address": address,
                "expected_date": expected_date
            }

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
            return

    # Function to display cart
    def cart_button():
        if not cart:  # if cart is empty
            messagebox.showinfo("Cart", "Your cart is empty.")
            return

        cart_details = "Items in Cart:\n"
        items_price = sum(item._price for item in cart)
        vat = items_price * 0.2
        delivery_fee = 7.99
        total_price = items_price + vat + delivery_fee
        for item in cart:
            cart_details += f"{item._title} - ${item._price:.2f}\n"
        cart_details += f"\nVAT: ${vat:.2f}\nShipping Fee: ${delivery_fee:.2f}\nTotal: ${total_price:.2f}"
        messagebox.showinfo("Cart", cart_details)

    # Checkout Function
    def checkout_button():
        if not cart:
            messagebox.showinfo("Checkout", "Your cart is empty.")
            return

        # Validate user data
        user_data = get_user_data()
        if not user_data:
            return

        # Process checkout
        items_price = sum(item._price for item in cart)
        vat = items_price * 0.2
        delivery_fee = 7.99
        total_price = items_price + vat + delivery_fee

        # final massage
        messagebox.showinfo("Your order has been placed!",
                            f"Expected Date of Arrival: {user_data['expected_date']}\n\nItems in Cart:\n{', '.join(item._title for item in cart)}\n\nTotal Amount: ${total_price:.2f}\n\nTHANK YOU!\n-QuirkByte")

        # End the program after checkout
        root1.destroy()

    # Create frame for books
    frame_books = tk.Frame(root1, bg="#121212")
    frame_books.pack(side="top", pady=20)

    label_books = tk.Label(frame_books, text="BOOKS", font=("Arial", 18, "bold"), bg="#121212", fg="#FFFFFF")
    label_books.pack(side="top", pady=(0, 10))

    for book in books:
        label_book = tk.Label(frame_books, text=f"{book._title} - ${book._price:.2f}", font=("Arial", 12), bg="#121212",
                              fg="#FFFFFF")
        button_details_book = tk.Button(frame_books, text="Details", command=lambda b=book: display_details(b),
                                        font=("Arial", 10), bg="#181818", fg="#FFFFFF")
        button_add_book = tk.Button(frame_books, text="Add to Cart", command=lambda b=book: add_to_cart(b), bg="#404040",
                                    fg="#FFFFFF", font=("Arial", 10))
        label_book.pack(side="left", padx=10)
        button_details_book.pack(side="left", padx=5)
        button_add_book.pack(side="left", padx=10)  # Adjusted padding here

    # Create frame for magazines
    frame_magazines = tk.Frame(root1, bg="#121212")
    frame_magazines.pack(side="top", pady=15)

    label_magazines = tk.Label(frame_magazines, text="MAGAZINES", font=("Arial", 18, "bold"), bg="#121212", fg="#FFFFFF")
    label_magazines.pack(side="top", pady=(0, 10))

    for magazine in magazines:
        label_magazine = tk.Label(frame_magazines, text=f"{magazine._title} - ${magazine._price:.2f}", font=("Arial", 12),
                                  bg="#121212", fg="#FFFFFF")
        button_details_magazine = tk.Button(frame_magazines, text="Details", command=lambda m=magazine: display_details(m),
                                            font=("Arial", 10), bg="#181818", fg="#FFFFFF")
        button_add_magazine = tk.Button(frame_magazines, text="Add to Cart", command=lambda m=magazine: add_to_cart(m),
                                        bg="#404040", fg="#FFFFFF", font=("Arial", 10))
        label_magazine.pack(side="left", padx=13)
        button_details_magazine.pack(side="left", padx=5)
        button_add_magazine.pack(side="left", padx=10)  # Adjusted padding here

    # Create frame for magazines
    frame_dvds = tk.Frame(root1, bg="#121212")
    frame_dvds.pack(side="top", pady=20)

    label_dvds = tk.Label(frame_dvds, text="DVDS", font=("Arial", 18, "bold"), bg="#121212", fg="#FFFFFF")
    label_dvds.pack(side="top", pady=(0, 15))

    for dvd in dvds:
        label_dvd = tk.Label(frame_dvds, text=f"{dvd._title} - ${dvd._price:.2f}", font=("Arial", 12), bg="#121212",
                             fg="#FFFFFF")
        button_details_dvd = tk.Button(frame_dvds, text="Details", command=lambda d=dvd: display_details(d),
                                       font=("Arial", 10), bg="#181818", fg="#FFFFFF")
        button_add_dvd = tk.Button(frame_dvds, text="Add to Cart", command=lambda d=dvd: add_to_cart(d), bg="#404040",
                                   fg="#FFFFFF", font=("Arial", 10))
        label_dvd.pack(side="left", padx=29)
        button_details_dvd.pack(side="left", padx=5)
        button_add_dvd.pack(side="left", padx=10)  # Adjusted padding here

    # Button to checkout
    button_checkout = tk.Button(root1, text="Checkout", command=checkout_button, bg="#B3B3B3", fg="#FFFFFF", font=("Arial", 12))
    button_checkout.pack(side="bottom", pady=10, padx=20, fill="x")

    # Button to view cart
    button_cart = tk.Button(root1, text="View Cart", command=cart_button, bg="#282828", fg="#FFFFFF", font=("Arial", 12))
    button_cart.pack(side="bottom", pady=10, padx=20, fill="x")

    # Call the function to update cart button text
    update_cart_button_text()

    root1.mainloop()


def create_admin_gui():
    # Creating main window for admins:
    pass_key = input("Enter Your Pass Key: ")
    if pass_key == "kali linux":
        root0 = tk.Tk()
        root0.title("QuirkByte's Admin Room")
        image = tk.PhotoImage(file="/home/huevvn/Documents/My Projects/Python Projects/My First Python Project/0.png")
        root0.geometry("1400x840")
        background_label = tk.Label(root0, image=image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        def on_escape(event):
            root0.destroy()

        # Letting tk define Esc button as the event which run "on_escape" function to quit program
        root0.bind("<Escape>", on_escape)

        # Function to add a new item to the library
        def add_item():
            item_type = simpledialog.askstring("Add Item", "Enter the type of item (book/magazine/dvd):")
            if item_type.lower() == "book":
                title = simpledialog.askstring("Add Book - Title", "Enter the title:")
                author = simpledialog.askstring("Add Book - Author", "Enter the author:")
                price = float(simpledialog.askstring("Add Book - Price", "Enter the price:"))
                rating = simpledialog.askstring("Add Book - Rating", "Enter the rating:")
                isbn = simpledialog.askstring("Add Book - ISBN", "Enter the ISBN:")
                genre = simpledialog.askstring("Add Book - Genre", "Enter the genre:")
                num_pages = int(simpledialog.askstring("Add Book - Pages", "Enter the number of pages:"))
                books.append(Book(title, author, price, rating, isbn, genre, num_pages))
                messagebox.showinfo("Success", "Book added successfully.")
            elif item_type.lower() == "magazine":
                title = simpledialog.askstring("Add Magazine - Title", "Enter the title:")
                price = float(simpledialog.askstring("Add Magazine - Price", "Enter the price:"))
                rating = simpledialog.askstring("Add Magazine - Rating", "Enter the rating:")
                issue_number = simpledialog.askstring("Add Magazine - Issue number", "Enter the issue number:")
                publication_date = simpledialog.askstring("Add Magazine - publication", "Enter the publication date:")
                editor = simpledialog.askstring("Add Magazine - Editor", "Enter the editor:")
                magazines.append(Magazine(title, price, rating, issue_number, publication_date, editor))
                messagebox.showinfo("Success", "Magazine added successfully.")
            elif item_type.lower() == "dvd":
                title = simpledialog.askstring("Add DVD - Title", "Enter the title:")
                price = float(simpledialog.askstring("Add DVD - Price", "Enter the price:"))
                rating = simpledialog.askstring("Add DVD - Rating", "Enter the rating:")
                director = simpledialog.askstring("Add DVD - Director", "Enter the director:")
                duration = simpledialog.askstring("Add DVD - Duration", "Enter the duration:")
                genre = simpledialog.askstring("Add DVD - Genre", "Enter the genre:")
                dvds.append(DVD(title, price, rating, director, duration, genre))
                messagebox.showinfo("Success", "DVD added successfully.")
            else:
                messagebox.showwarning("Warning", "Invalid item type.")

        # Function to edit an existing item in the library
        def edit_item():
            item_type = simpledialog.askstring("Edit Item", "Enter the type of item to edit (book/magazine/dvd):")
            if item_type.lower() == "book":
                title = simpledialog.askstring("Edit Book", "Enter the title of the book to edit:")
                for book in books:
                    if book._title == title:
                        book._title = simpledialog.askstring("Edit Book - Title", "Enter the new title:")
                        book._author = simpledialog.askstring("Edit Book - Author", "Enter the new author:")
                        book._price = float(simpledialog.askstring("Edit Book - Price", "Enter the new price:"))
                        book._rating = simpledialog.askstring("Edit Book - Rating", "Enter the new rating:")
                        book._isbn = simpledialog.askstring("Edit Book - ISBN", "Enter the new ISBN:")
                        book._genre = simpledialog.askstring("Edit Book - Genre", "Enter the new genre:")
                        book._number_of_pages = int(simpledialog.askstring("Edit Book - Pages", "Enter the new number of pages:"))
                        messagebox.showinfo("Success", "Book edited successfully.")
                        break
                else:
                    messagebox.showwarning("Warning", "Book not found.")
            elif item_type.lower() == "magazine":
                title = simpledialog.askstring("Edit Magazine", "Enter the title of the magazine to edit:")
                for magazine in magazines:
                    if magazine._title == title:
                        magazine._title = simpledialog.askstring("Edit Magazine - Title", "Enter the new title:")
                        magazine._price = float(simpledialog.askstring("Edit Magazine - Rating", "Enter the new price:"))
                        magazine._rating = simpledialog.askstring("Edit Magazine - Rating", "Enter the new rating:")
                        magazine._issue_number = simpledialog.askstring("Edit Magazine - Issue Number", "Enter the new issue number:")
                        magazine._publication_date = simpledialog.askstring("Edit Magazine - Publication ", "Enter the new publication date:")
                        magazine._editor = simpledialog.askstring("Edit Magazine - Editor", "Enter the new editor:")
                        messagebox.showinfo("Success", "Magazine edited successfully.")
                        break
                else:
                    messagebox.showwarning("Warning", "Magazine not found.")
            elif item_type.lower() == "dvd":
                title = simpledialog.askstring("Edit DVD", "Enter the title of the DVD to edit:")
                for dvd in dvds:
                    if dvd._title == title:
                        dvd._title = simpledialog.askstring("Edit DVD - Title", "Enter the new title:")
                        dvd._price = float(simpledialog.askstring("Edit DVD - Price", "Enter the new price:"))
                        dvd._rating = simpledialog.askstring("Edit DVD - Rating", "Enter the new rating:")
                        dvd._director = simpledialog.askstring("Edit DVD - Director", "Enter the new director:")
                        dvd._duration = simpledialog.askstring("Edit DVD - Duration", "Enter the new duration:")
                        dvd._genre = simpledialog.askstring("Edit DVD - Genre", "Enter the new genre:")
                        messagebox.showinfo("Success", "DVD edited successfully.")
                        break
                else:
                    messagebox.showwarning("Warning", "DVD not found.")
            else:
                messagebox.showwarning("Warning", "Invalid item type.")

        # Function to delete an item from the library
        def delete_item():
            item_type = simpledialog.askstring("Delete Item", "Enter the type of item to delete (book/magazine/dvd):")
            if item_type.lower() == "book":
                title = simpledialog.askstring("Delete Book", "Enter the title of the book to delete:")
                for book in books:
                    if book._title == title:
                        books.remove(book)
                        messagebox.showinfo("Success", "Book deleted successfully.")
                        break
                else:
                    messagebox.showwarning("Warning", "Book not found.")
            elif item_type.lower() == "magazine":
                title = simpledialog.askstring("Delete Magazine", "Enter the title of the magazine to delete:")
                for magazine in magazines:
                    if magazine._title == title:
                        magazines.remove(magazine)
                        messagebox.showinfo("Success", "Magazine deleted successfully.")
                        break
                else:
                    messagebox.showwarning("Warning", "Magazine not found.")
            elif item_type.lower() == "dvd":
                title = simpledialog.askstring("Delete DVD", "Enter the title of the DVD to delete:")
                for dvd in dvds:
                    if dvd._title == title:
                        dvds.remove(dvd)
                        messagebox.showinfo("Success", "DVD deleted successfully.")
                        break
                else:
                    messagebox.showwarning("Warning", "DVD not found.")
            else:
                messagebox.showwarning("Warning", "Invalid item type.")

        # Button to switch to User GUI
        button_switch_to_user_gui = tk.Button(root0, text="Switch to User GUI",
                                              command=lambda: [root0.destroy(), create_customer_gui()],
                                              bg="#0086D0", fg="#000000", font=("Arial", 12))
        button_switch_to_user_gui.pack(side="bottom", pady=10, padx=20, fill="x")

        # Button to delete item
        button_delete = tk.Button(root0, text="Delete Item", command=delete_item, bg="#B3B3B3", fg="#000000",
                                  font=("Arial", 12))
        button_delete.pack(side="bottom", pady=10, padx=20, fill="x")

        # Button to edit item
        button_edit = tk.Button(root0, text="Edit Item", command=edit_item, bg="#B3B3B3", fg="#000000", font=("Arial", 12))
        button_edit.pack(side="bottom", pady=10, padx=20, fill="x")

        # Button to add item
        button_add = tk.Button(root0, text="Add Item", command=add_item, bg="#B3B3B3", fg="#000000", font=("Arial", 12))
        button_add.pack(side="bottom", pady=10, padx=20, fill="x")

        root0.mainloop()

    else:
        print("*Wrong Password*\nHint: The best OS for hackers")


# Admin OR Customer?
s = input("For Customers Press 1 .. For Administrators Press 0: ")

if s == "1":
    create_customer_gui()

elif s == "0":
    create_admin_gui()

else:
    print("No User Matched!")
