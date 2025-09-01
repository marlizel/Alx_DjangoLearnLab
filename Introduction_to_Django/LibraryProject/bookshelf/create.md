# Create a Book instance

```python
from bookshelf.models import Book

# Create a new book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Check the ID of the created book
book.id  # Expected output: 1 (or the primary key of the new row)
