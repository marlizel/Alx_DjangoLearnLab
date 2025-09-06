# relationship_app/urls.py

from django.urls import path
from .views import list_books, register_view, home
from django.contrib.auth.views import LoginView, LogoutView
from .views import LibraryDetailView

urlpatterns = [
    # General app views
    path('', home, name='home'),
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views
    # Use built-in LoginView and LogoutView
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    # Use our custom registration view
    path('register/', register_view, name='register'),
]