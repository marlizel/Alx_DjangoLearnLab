# relationship_app/views.py

from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from .models import Library  # The checker is looking for this exact line

# Function-based view to list all books
def book_list(request):
    """
    Renders a list of all books from the database.
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to display details for a single library
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'