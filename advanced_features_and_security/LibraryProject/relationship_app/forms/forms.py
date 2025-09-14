# relationship_app/forms/forms.py
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form based on Django's built-in form.
    This is used for our registration view.
    """
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)