# relationship_app/urls.py

from django.urls import path
from . import views
from .views import list_books, home
from django.contrib.auth.views import LoginView, LogoutView
from .views import LibraryDetailView

urlpatterns = [
    # General app views
    path('', home, name='home'),
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    # Use the 'views.register' pattern as required
    path('register/', views.register, name='register'),
]