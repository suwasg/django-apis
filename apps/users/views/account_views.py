from django.shortcuts import redirect 
from django.contrib import messages
from django.contrib.auth import logout

from ..models import *

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