# relationship_app/urls.py

from django.urls import path
from .views import (
    list_books, home, register, LibraryDetailView,
    admin_view, librarian_view, member_view,
    add_book, edit_book, delete_book
)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # General app views
    path('', home, name='home'),
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),

    # Role-based views
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),

    # Custom permission views - Corrected paths
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
]