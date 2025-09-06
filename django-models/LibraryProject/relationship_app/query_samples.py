# relationship_app/query_samples.py

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings') # Change 'django_models' to your project's name
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

print("--- 1. Query all books by a specific author (Jane Doe) ---")
# Use the filter() method with the related object
# We can use the reverse relationship, which Django automatically creates.
books_by_jane = Book.objects.filter(author__name="Jane Doe")
for book in books_by_jane:
    print(f"Title: {book.title}, Author: {book.author.name}")
print("\n")


print("--- 2. List all books in a library (Central Library) ---")
# Retrieve the Library object first
central_library = Library.objects.get(name="Central Library")
# Then access the related books using the ManyToManyField
books_in_library = central_library.books.all()
for book in books_in_library:
    print(f"Title: {book.title}")
print("\n")


print("--- 3. Retrieve the librarian for a library (Central Library) ---")
# Retrieve the Library object
central_library = Library.objects.get(name="Central Library")
# Access the related Librarian object using the reverse relationship defined by OneToOneField
librarian_for_library = central_library.librarian
print(f"The librarian for {central_library.name} is {librarian_for_library.name}.")