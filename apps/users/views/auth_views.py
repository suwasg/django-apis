from django.shortcuts import render, redirect 
# render: Combines a template with a context dictionary and returns an HttpResponse.
# redirect: Redirects to another URL (usually after form submission).
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from ..models import *

from ..forms import CustomUserCreationForm, LoginForm
# Create your views here.
def register_view(request):
    if request.method == 'POST': # If the form is submitted (i.e., form uses method="POST"), process the data.
        form = CustomUserCreationForm(request.POST, request.FILES) # Instantiate the registration form with submitted data. Also handles file input (like profile images).
        if form.is_valid(): # form.is_valid() checks if all form validations pass.
            form.save() # If yes, save the new user to the database.
            messages.success(request, "Account created successfully! Please login to continue.")
            return redirect('login') # Then, redirect to the login page (URL named 'login').
    else: # If GET request (i.e., page load), initialize an empty registration form.
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form':form}) # Render the registration form template with the form context.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  # already logged in

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome { user.first_name}!")
            return redirect('profile')
        else:
            messages.error(request, "Login failed.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('login')



