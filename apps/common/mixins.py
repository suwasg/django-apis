from django.contrib import messages
from django.shortcuts import render, redirect 

class SuccessMessageMixin:
    """"
    A mixin that adds a success message when saving an object.
    This can be used in views to provide feedback to the user after a successful operation.
    """
    success_message = None 
    def form_valid(self, form):
       response = super().form_valid(form)  # Call the parent class's form_valid method to save the form.
       if self.success_message:
              messages.success(self.request, self.success_message)
       return response

class LoginRequiredMixin:
    """
    A mixin that requires the user to be logged in to access the view.
    If the user is not authenticated, they will be redirected to the login page.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('user/login')  # Redirect to the login page if not authenticated
        return super().dispatch(request, *args, **kwargs)
        