from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# render: Combines a template with a context dictionary and returns an HttpResponse.
# redirect: Redirects to another URL (usually after form submission).

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
        return redirect('/')  # redirect to home if already logged in

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # or email if using email as login
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.get_full_name() or user.first_name} !")
                return redirect('home')  
            else:
                messages.error(request, "Identifiants invalides.")
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier les champs.")
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})