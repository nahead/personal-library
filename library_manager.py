import streamlit as st
import json
import os

data_file = "library.txt"

def load_library():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.warning("Library data is corrupted. Starting with a new library.")
            return []
    return []

def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file)

def add_book(library):
    with st.form("Add Book"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.text_input("Year")
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        submitted = st.form_submit_button("Add Book")
        if submitted:
            new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
            library.append(new_book)
            save_library(library)
            st.success(f"Book '{title}' added successfully.")

def remove_book(library):
    title = st.text_input("Enter the title of the book to delete").lower()
    if st.button("Remove Book"):
        initial_length = len(library)
        updated_library = [book for book in library if book["title"].lower() != title]
        if len(updated_library) < initial_length:
            save_library(updated_library)
            library.clear()
            library.extend(updated_library)
            st.success(f"Book '{title}' has been removed from the library.")
        else:
            st.error(f"Book '{title}' was not found in the library.")

def search_library(library):
    search_by = st.radio("Search by", ["Title", "Author"]).lower()
    search_term = st.text_input(f"Enter the {search_by}").lower()
    if st.button("Search"):
        results = [book for book in library if search_term in book[search_by].lower()]
        if results:
            for book in results:
                status = "read" if book["read"] else "unread"
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.error(f"No books found matching '{search_term}' in the {search_by} field.")

def display_library(library):
    if library:
        for book in library:
            status = "read" if book["read"] else "unread"
            st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} is {status}")
    else:
        st.info("No books in the library.")

def display_statistics(library):
    total_books = len(library)
    total_read_books = len([book for book in library if book["read"]])
    percentage_count = (total_read_books / total_books) * 100 if total_books > 0 else 0
    st.write(f"Total books in the library: {total_books}")
    st.write(f"{percentage_count:.2f}% of the books have been read.")

def main():
    st.title("Library Manager")
    library = load_library()

    menu = ["Add Book", "Remove Book", "Search Book", "Display All Books", "Display Statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Book":
        add_book(library)
    elif choice == "Remove Book":
        remove_book(library)
    elif choice == "Search Book":
        search_library(library)
    elif choice == "Display All Books":
        display_library(library)
    elif choice == "Display Statistics":
        display_statistics(library)

if __name__ == "__main__":
    main()
