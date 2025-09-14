# Update the Book instance

```python
from bookshelf.models import Book

# Retrieve the book first
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm update
Book.objects.get(id=book.id).title
# Expected output: 'Nineteen Eighty-Four'
