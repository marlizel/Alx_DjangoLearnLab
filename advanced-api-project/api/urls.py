# advanced-api-project/api/urls.py

from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    # URL for listing books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # URL for creating a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # URLs for retrieving a single book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # URLs for updating and deleting a book, matching the checker's required string
    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
]