from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home Page
    path("", views.home, name="home"),
    
    # Registration
    path("register/", views.register, name="register"),
    
    # Login/Logout (using built-in views)
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Profile Management
    path('profile/', views.profile, name='profile'),
]