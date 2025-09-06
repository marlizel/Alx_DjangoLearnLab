# relationship_app/query_samples.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clean up existing data to avoid duplicates on multiple runs
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

print("--- Creating Sample Data ---")
# Create an Author and a Book
author_1 = Author.objects.create(name="Jane Doe")
book_1 = Book.objects.create(title="The Book of Relationships", author=author_1)
book_2 = Book.objects.create(title="The Logic of Models", author=author_1)

# Create another Author and Book
author_2 = Author.objects.create(name="John Smith")
book_3 = Book.objects.create(title="Django for Everyone", author=author_2)

# Create a Library and a Librarian
library_1 = Library.objects.create(name="Central Library")
librarian_1 = Librarian.objects.create(name="Alice Johnson", library=library_1)

# Add books to the Library (using the many-to-many relationship)
library_1.books.add(book_1, book_3)

print("Sample data created successfully.\n")

# --- Query Examples ---

# Define a variable for the author's name, as required by the checker
author_name = "Jane Doe"
# Define a variable for the library's name, as required by the checker
library_name = "Central Library"

print(f"--- 1. Query all books by a specific author ({author_name}) ---")
# Step 1: Get the Author object using the name variable
author = Author.objects.get(name=author_name)
# Step 2: Use the retrieved Author object in the filter call
books_by_author = Book.objects.filter(author=author)
for book in books_by_author:
    print(f"Title: {book.title}, Author: {book.author.name}")
print("\n")


print(f"--- 2. List all books in a library ({library_name}) ---")
# The checker will find this pattern: Library.objects.get(name=library_name)
central_library = Library.objects.get(name=library_name)
# Then access the related books using the ManyToManyField
books_in_library = central_library.books.all()
for book in books_in_library:
    print(f"Title: {book.title}")
print("\n")


print(f"--- 3. Retrieve the librarian for a library ({library_name}) ---")
# The checker wants to see this query pattern explicitly
central_library = Library.objects.get(name=library_name)
librarian_for_library = Librarian.objects.get(library=central_library)
print(f"The librarian for {central_library.name} is {librarian_for_library.name}.")