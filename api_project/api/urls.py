# api_project/api/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookList, BookViewSet # Make sure both views are imported

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Route for the BookList view (from Task 1)
    path('books/', BookList.as_view(), name='book-list'),
    
    # Include the router URLs for BookViewSet (for CRUD operations)
    path('', include(router.urls)),
]