from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser , Business

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'name', 'description', 'category', 'address', 'city', 
            'postal_code', 'phone_number', 'email', 'website', 
            'image', 'latitude', 'longitude'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full p-2 border border-gray-300 rounded'}),
            'category': forms.TextInput(attrs={'class': 'mt-1 block w-full p-2 border border-gray-300 rounded'}),
            'address': forms.TextInput(attrs={'class': 'mt-1 block w-full p-2 border border-gray-300 rounded'}),
            # Add classes for other fields if needed
        }
