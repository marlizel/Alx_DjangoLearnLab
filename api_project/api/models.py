# api_project/api/models.py

from django.db import models

class Book(models.Model):
    """
    A simple model to represent a book.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.title} by {self.author}"