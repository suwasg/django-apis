"""
You create forms.py when you need custom forms to handle user input on the frontend (HTML pages), like:
- Registering users
- Editing profiles
- Adding addresses
- Contact forms
- Filtering/searching data
Django has a powerful form system (ModelForm) that connects your database models with the frontend form automatically
"""
from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Address

# For registering new users.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_image']

# For updating user info.
class CustomUserChangeForm(UserChangeForm):
    password = None # Optional field. Not show on updating user profile.
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'profile_image']

# Address Form
class AddressForm(forms.ModelForm):
    class Meta: 
        model = Address
        fields = ['address_type', 'city', 'state', 'postal_code', 'country']