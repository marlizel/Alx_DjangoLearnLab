# relationship_app/views.py

from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .models import Book, Library
from .forms.forms import CustomUserCreationForm # Import the custom form

# A simple view for the home page after login
def home(request):
    """
    Placeholder home view.
    """
    return render(request, 'relationship_app/home.html')

# Function-based view to list all books
def list_books(request):
    """
    Renders a list of all books from the database.
    """
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to display details for a single library
class LibraryDetailView(DetailView):
    """
    Displays details for a specific library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Function-based view for user registration
def register_view(request):
    """
    Handles user registration using a custom form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # Redirect to a homepage after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})