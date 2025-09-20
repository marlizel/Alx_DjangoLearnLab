# api_project/api/views.py

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    # This specifies the queryset of objects to be returned.
    # We are getting all objects from the Book model.
    queryset = Book.objects.all()
    
    # This links the view to the serializer we just created.
    serializer_class = BookSerializer