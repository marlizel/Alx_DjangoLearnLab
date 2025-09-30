from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # --- Authentication URLs (from Task 1) ---
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # --- Blog Post CRUD URLs (Task 2) ---
    
    # List all posts
    path('posts/', PostListView.as_view(), name='posts'),
    
    # Create new post
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    
    # Detail view of a single post (uses primary key: pk)
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    # Update existing post
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    
    # Delete existing post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]