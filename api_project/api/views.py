# api_project/api/views.py

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # Add this import
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    # This specifies the queryset of objects to be returned.
    # We are getting all objects from the Book model.
    queryset = Book.objects.all()
    
    # This links the view to the serializer we just created.
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Add this line