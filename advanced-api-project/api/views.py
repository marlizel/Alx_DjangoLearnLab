# advanced-api-project/api/views.py

from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# This view is for retrieving all books.
class BookListView(generics.ListAPIView):
    """
    A generic view for listing all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Allows read-only access to unauthenticated users

# This view is for retrieving a single book by ID.
class BookDetailView(generics.RetrieveAPIView):
    """
    A generic view for retrieving a single book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Allows read-only access to unauthenticated users

# This view is for creating a new book.
class BookCreateView(generics.CreateAPIView):
    """
    A generic view for creating a new book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can create

# This view is for updating an existing book.
class BookUpdateView(generics.UpdateAPIView):
    """
    A generic view for updating an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can update

# This view is for deleting a book.
class BookDeleteView(generics.DestroyAPIView):
    """
    A generic view for deleting a book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can delete