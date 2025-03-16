import streamlit as st
import json
import os

FILE_NAME = "library.json"

# Function to load books from file
def load_books():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            books = json.load(file)
            # Ensure all books have a 'publish_year'
            for book in books:
                if 'publish_year' not in book:
                    book['publish_year'] = 2000  # Set a default value (2000, for example)
            return books
    return []

# Function to save books to file
def save_books(library):
    with open(FILE_NAME, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_books()

# Custom CSS for Colorful UI
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .book {
        background: linear-gradient(135deg, #ff7eb3, #ff758c);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: white;
        font-weight: bold;
    }
    .title {
        font-size: 18px;
    }
    .author {
        font-size: 14px;
        color: #ffe6e6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📚 Library Management")

# Sidebar Menu
menu = st.sidebar.radio("Menu", ["View Books", "Add Book", "Delete Book", "Edit Book", "Search Book"])

# Sidebar Categories
st.sidebar.subheader("Categories")
categories = ["All Books", "Islamiat", "Poetry", "Grammar", "Coding", "Software Engineering"]
selected_category = st.sidebar.radio("Select Category", categories)

# View Books
if menu == "View Books":
    st.header("📖 All Books")
    categorized_books = {category: [] for category in categories[1:]}
    
    for book in library:
        category = book.get("category", "Software Engineering")  # Default category fix
        categorized_books.setdefault(category, []).append(book)
    
    if selected_category == "All Books":
        for category, books in categorized_books.items():
            st.subheader(category)
            if books:
                for book in books:
                    st.markdown(
                        f"""
                        <div class="book">
                            <div>
                                <p class="title"><a href="{book['link']}" target="_blank" style="color: white; text-decoration: none;">{book['title']}</a></p>
                                <p class="author">by {book['author']} - Published: {book['publish_year']} - Category: {book['category']}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.write("No books available in this category!")
    else:
        st.subheader(selected_category)
        books = categorized_books.get(selected_category, [])
        if books:
            for book in books:
                st.markdown(
                    f"""
                    <div class="book">
                        <div>
                            <p class="title"><a href="{book['link']}" target="_blank" style="color: white; text-decoration: none;">{book['title']}</a></p>
                            <p class="author">by {book['author']} - Published: {book['publish_year']} - Category: {book['category']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.write("No books available in this category!")

# Add Book
elif menu == "Add Book":
    st.subheader("➕ Add a Book")
    book_title = st.text_input("Book Title")
    book_author = st.text_input("Author")
    book_link = st.text_input("Book Link")
    book_category = st.selectbox("Category", categories[1:])  # Correct category selection
    book_publish_year = st.number_input("Publishing Year", min_value=1000, max_value=2100, step=1)

    if st.button("Add Book") and book_title and book_author and book_link:
        new_book = {
            "title": book_title,
            "author": book_author,
            "link": book_link,
            "category": book_category,  # Category correctly assigned
            "publish_year": book_publish_year,  # Add the publish year
        }
        library.append(new_book)
        save_books(library)
        
        # Success Popup
        st.success(f"✅ Book '{book_title}' Added to {book_category}!")
        st.toast(f"🎉 '{book_title}' successfully added!", icon="📚")
        
        st.rerun()

# Delete Book
elif menu == "Delete Book":
    st.subheader("❌ Delete a Book")
    delete_category = st.selectbox("Select Category to Delete From", categories[1:])
    categorized_books = {category: [] for category in categories}
    for book in library:
        categorized_books.setdefault(book['category'], []).append(book)
    books_in_delete_category = [book["title"] for book in categorized_books.get(delete_category, [])]

    if books_in_delete_category:
        book_to_delete = st.selectbox("Select Book", books_in_delete_category)
        if st.button("Delete"):
            library = [book for book in library if book["title"] != book_to_delete or book["category"] != delete_category]
            save_books(library)
            st.success("✅ Book Deleted!")
            st.rerun()
    else:
        st.write("No books available in this category to delete!")

# Edit Book
elif menu == "Edit Book":
    st.subheader("✏️ Edit a Book")
    edit_category = st.selectbox("Select Category to Edit From", categories[1:])
    categorized_books = {category: [] for category in categories}
    for book in library:
        categorized_books.setdefault(book['category'], []).append(book)
    books_in_edit_category = [book["title"] for book in categorized_books.get(edit_category, [])]

    if books_in_edit_category:
        book_to_edit = st.selectbox("Select Book", books_in_edit_category)
        selected_book = next(book for book in library if book["title"] == book_to_edit)
        
        # Display current values
        st.write(f"**Current Title:** {selected_book['title']}")
        st.write(f"**Current Author:** {selected_book['author']}")
        st.write(f"**Current Link:** {selected_book['link']}")
        st.write(f"**Current Category:** {selected_book['category']}")
        st.write(f"**Current Publishing Year:** {selected_book['publish_year']}")

        # Edit fields
        new_title = st.text_input("New Title", value=selected_book["title"])
        new_author = st.text_input("New Author", value=selected_book["author"])
        new_link = st.text_input("New Book Link", value=selected_book["link"])
        new_category = st.selectbox("New Category", categories[1:], index=categories[1:].index(selected_book["category"]))
        new_publish_year = st.number_input("New Publishing Year", value=selected_book["publish_year"], min_value=1000, max_value=2100)

        if st.button("Update Book"):
            selected_book["title"] = new_title
            selected_book["author"] = new_author
            selected_book["link"] = new_link
            selected_book["category"] = new_category
            selected_book["publish_year"] = new_publish_year

            save_books(library)
            st.success(f"✅ Book '{new_title}' Updated!")
            st.rerun()
    else:
        st.write("No books available in this category to edit!")

# Search Book
elif menu == "Search Book":
    st.subheader("🔍 Search a Book")
    search_query = st.text_input("Enter book title or category to search")

    if search_query:
        search_results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["category"].lower()]
        if search_results:
            st.subheader("📌 Search Results:")
            for book in search_results:
                st.write(f"📖 **{book['title']}** by {book['author']} - Published: {book['publish_year']} - Category: {book['category']}")
        else:
            st.warning("⚠️ No book found!")
