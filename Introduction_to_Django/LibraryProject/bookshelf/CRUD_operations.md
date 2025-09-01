```python
from bookshelf.models import Book

# CREATE
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book.id  # Expected output: 1 (or the ID assigned in the database)

# RETRIEVE
book = Book.objects.get(title="1984")
(book.title, book.author, book.publication_year)
# Expected output: ('1984', 'George Orwell', 1949)

# UPDATE
book.title = "Nineteen Eighty-Four"
book.save()
Book.objects.get(id=book.id).title
# Expected output: 'Nineteen Eighty-Four'

# DELETE
book.delete()
Book.objects.all()
# Expected output: <QuerySet []>
