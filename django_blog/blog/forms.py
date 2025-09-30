from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration, explicitly including the email field 
    and ensuring it's required for new users.
    """
    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserCreationForm.Meta):
        # Use the built-in User model
        model = User
        # Define the fields shown during registration
        fields = ('username', 'email', 'first_name', 'last_name')
        
    def save(self, commit=True):
        """
        Overrides save to ensure the email is captured and saved correctly.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """
    Form for authenticated users to edit their core User details (name, email).
    This form is used in the profile view.
    """
    email = forms.EmailField(required=True, label="Email Address")
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populates the email field with the current user's email for editing
        if self.instance and self.instance.email:
            self.initial['email'] = self.instance.email


class ProfileBioForm(forms.ModelForm):
    """
    Form to edit the custom Profile model (bio).
    """
    class Meta:
        model = Profile
        fields = ('bio',)
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}), # Use a larger input box for bio
        }
