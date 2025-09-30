from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView,
    # --- NEW: Import Comment Views for Task 3 ---
    CommentCreateView,  # <-- ADDED THIS IMPORT
    CommentUpdateView,
    CommentDeleteView
)

urlpatterns = [
    # --- Authentication URLs (Task 1) ---
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # --- Blog Post CRUD URLs (Task 2) ---
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # --- NEW: Comment CRUD URLs (Task 3) ---
    # Create new comment on a specific post (uses post's pk)
    path('posts/<int:pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    
    # Update existing comment by its primary key (pk)
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    
    # Delete existing comment by its primary key (pk)
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
