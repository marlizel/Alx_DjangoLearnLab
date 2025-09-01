# Retrieve the Book instance

```python
from bookshelf.models import Book

# Retrieve the book we just created
book = Book.objects.get(title="1984")

# Display all attributes
(book.title, book.author, book.publication_year)
# Expected output: ('1984', 'George Orwell', 1949)
