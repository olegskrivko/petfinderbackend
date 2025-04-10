# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import CustomUser
from authentication.utils import generate_hex_username 

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'avatar_animal']  # Include necessary fields

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            # Automatically generate a username if one is not provided
            username = generate_hex_username()
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Set the password
        if commit:
            user.save()
        return user
