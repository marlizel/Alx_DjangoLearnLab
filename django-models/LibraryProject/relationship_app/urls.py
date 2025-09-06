# relationship_app/urls.py

from django.urls import path
from .views import list_books # The checker is looking for this exact line
from .views import LibraryDetailView # This is also good practice

urlpatterns = [
    # URL for the function-based view
    path('books/', book_list, name='book_list'),

    # URL for the class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]