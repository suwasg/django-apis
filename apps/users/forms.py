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
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models.user import CustomUser, UserSettings
from .models.address import Address
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

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

# login form
# class LoginForm(AuthenticationForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password']


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password.")
            self.user = user  # Store the user for later use in the view
        return cleaned_data

    def get_user(self):
        return self.user

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = [
            'receive_emails',
            'dark_mode',
            'show_email_publicly',
            'show_phone_number_publicly',
            'show_date_of_birth_publicly',
            'show_profile_image_publicly',
            'show_full_name_publicly',
            'show_last_login',
            'show_date_joined',
        ]
        widgets = {
            'receive_emails': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'dark_mode': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_email_publicly': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_phone_number_publicly': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_date_of_birth_publicly': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_profile_image_publicly': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_full_name_publicly': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_last_login': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'show_date_joined': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'receive_emails': "Receive Email Notifications",
            'dark_mode': "Enable Dark Mode",
            'show_email_publicly': "Show Email to Public",
            'show_phone_number_publicly': "Show Phone Number to Public",
            'show_date_of_birth_publicly': "Show Date of Birth to Public",
            'show_profile_image_publicly': "Show Profile Image to Public",
            'show_full_name_publicly': "Show Full Name to Public",
            'show_last_login': "Show Last Login Time",
            'show_date_joined': "Show Account Creation Date",
        }
        help_texts = {
            'receive_emails': "Turn on to get updates and notifications.",
            'dark_mode': "Switch between light and dark theme.",
        }

# Address Form
class AddressForm(forms.ModelForm):
    class Meta: 
        model = Address
        fields = ['address_type','street', 'city', 'state', 'postal_code', 'country']