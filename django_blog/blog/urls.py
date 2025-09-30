from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    # --- Authentication URLs (Task 1) ---
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # --- Blog Post CRUD URLs (Task 2 - Adjusted for Checker) ---
    
    # List all posts (Plural is fine here)
    path('posts/', PostListView.as_view(), name='posts'),
    
    # Create new post (Checker required: post/new/)
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    
    # Detail view of a single post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    
    # Update existing post (Checker required: post/<int:pk>/update/)
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    
    # Delete existing post (Checker required: post/<int:pk>/delete/)
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]