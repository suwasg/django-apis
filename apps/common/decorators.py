from django.shortcuts import render, redirect
from functools import wraps

def superuser_required(view_func):
    """
    Decorator to ensure that the user is a superuser.
    If the user is not a superuser, they will be redirected to the home page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')  # Redirect to home if not a superuser
        return view_func(request, *args, **kwargs)
    return _wrapped_view