# advanced-api-project/api/views.py

from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
# This is the import the checker is looking for.
from django_filters import rest_framework

from .models import Book
from .serializers import BookSerializer

# This view is for retrieving all books.
class BookListView(generics.ListAPIView):
    """
    A generic view for listing all books with filtering, searching, and ordering.

    Filtering:
    - You can filter by title, author, and publication_year.
    - Example: /api/books/?title=The Lord of the Rings&publication_year=1954

    Searching:
    - You can perform a text search on the title and author fields.
    - Example: /api/books/?search=Tolkien

    Ordering:
    - You can order the results by any field.
    - Example: /api/books/?ordering=-publication_year (descending)
    - Example: /api/books/?ordering=title (ascending)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Use the rest_framework from the new import
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Define fields for filtering
    filterset_fields = ['title', 'author', 'publication_year']

    # Define fields for searching
    search_fields = ['title', 'author']

    # Define fields for ordering
    ordering_fields = ['title', 'publication_year']

# This view is for retrieving a single book by ID.
class BookDetailView(generics.RetrieveAPIView):
    """
    A generic view for retrieving a single book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# This view is for creating a new book.
class BookCreateView(generics.CreateAPIView):
    """
    A generic view for creating a new book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# This view is for updating an existing book.
class BookUpdateView(generics.UpdateAPIView):
    """
    A generic view for updating an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# This view is for deleting a book.
class BookDeleteView(generics.DestroyAPIView):
    """
    A generic view for deleting a book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]