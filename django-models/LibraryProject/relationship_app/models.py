# relationship_app/models.py
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    # This creates a one-to-many relationship.
    # One Author can have many Books.
    # If the Author is deleted, all their Books are also deleted (CASCADE).
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField(default=2023)

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100)
    # This creates a many-to-many relationship.
    # One Library can have many Books, and one Book can belong to many Libraries.
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    # This creates a one-to-one relationship.
    # One Librarian can manage exactly one Library.
    # The 'related_name' allows us to easily access the Librarian from the Library object.
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name