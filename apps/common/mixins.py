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