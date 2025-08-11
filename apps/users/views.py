from django.shortcuts import render, redirect 
# render: Combines a template with a context dictionary and returns an HttpResponse.
# redirect: Redirects to another URL (usually after form submission).
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *

from .forms import CustomUserCreationForm, CustomUserChangeForm, AddressForm, LoginForm
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

@login_required
def profile_view(request):
    user = request.user
    addresses = Address.objects.filter(user = user)
    # return render(request, 'profile.html', {'user':user, 'addresses':addresses})
    context = {
        'user': user,
        'addresses' : addresses
    }
    return render(request, 'users/profile.html', context)
    

def profile_update_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance = request.user)  # The instance=request.user binds the form to the logged-in user's instance, so it updates rather than creates.

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:  # If GET, load the current user data into the form.
        form = CustomUserChangeForm(instance =  request.user)
    return render(request, 'profile_update.html', {'form':form})


def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST) # If form is submitted, populate with POST data.

        if form.is_valid():
            address = form.save(commit = False) # If valid, create an address object but don’t save it yet (commit=False). You do this because you still need to assign the user.
            address.user =  request.user # Attach the currently logged-in user to the address.
            address.save() # Save the address.
            return redirect('profile') # Redirect to the profile page.

    else: # For GET request, create an empty address form.
        form = AddressForm()
    return render(request, 'add_address.html', {'form':form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/users/profile')  # already logged in

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome { user.first_name}!")
            return redirect('/users/profile')
        else:
            messages.error(request, "Login failed.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out!")
    return redirect('login')

def deactivate_account_view(request):
    user = request.user
    user.is_active = False
    user.save()
    logout(request)
    messages.success(request, "Your account has been deactivated.")
    return redirect('login')

def delete_account_view(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been deleted.")
    return redirect('register')

