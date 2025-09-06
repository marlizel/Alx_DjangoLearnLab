# relationship_app/views.py

from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Library
from .forms.forms import CustomUserCreationForm
from .models import UserProfile # Import the UserProfile model

# Function to check for 'Admin' role
def is_admin(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False

# Function to check for 'Librarian' role
def is_librarian(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False

# Function to check for 'Member' role
def is_member(user):
    try:
        return user.is_authenticated and user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False

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
def register(request):
    """
    Handles user registration using a custom form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Role-based views with access decorators
@user_passes_test(is_admin)
def admin_view(request):
    """
    View accessible only to Admin users.
    """
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    """
    View accessible only to Librarian users.
    """
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    """
    View accessible only to Member users.
    """
    return render(request, 'relationship_app/member_view.html')