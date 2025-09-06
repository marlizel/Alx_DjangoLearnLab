# relationship_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL for the function-based view
    # e.g., /books/
    path('books/', views.book_list, name='book_list'),

    # URL for the class-based view
    # e.g., /library/1/ (where 1 is the library's primary key)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]