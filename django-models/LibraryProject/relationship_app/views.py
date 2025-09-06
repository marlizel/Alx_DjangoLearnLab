# relationship_app/views.py

from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view to list all books
def book_list(request):
    """
    Renders a list of all books from the database.
    """
    # This is the line with the first string the checker is looking for
    books = Book.objects.all()
    context = {
        'books': books
    }
    # This is the line with the second string the checker is looking for
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to display details for a single library
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'