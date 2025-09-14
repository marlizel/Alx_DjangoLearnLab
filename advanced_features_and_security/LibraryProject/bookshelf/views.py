# bookshelf/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'bookshelf/book_list.html', context)