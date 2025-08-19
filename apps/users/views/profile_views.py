from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import *
from ..forms import  CustomUserChangeForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

@login_required
def profile_view(request):
    user = request.user
    addresses = Address.objects.filter(user = user)
    settings = UserSettings.objects.filter(user = user)
    # return render(request, 'profile.html', {'user':user, 'addresses':addresses})
    context = {
        'user': user,
        'addresses' : addresses,
        'settings': settings,
    }
    return render(request, 'users/profile.html', context)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get user info
        user = self.request.user
        context["user"] = user

        # Get addresses
        context["addresses"] = Address.objects.filter(user=user)

        # ✅ Ensure settings always exist
        settings_obj, created = UserSettings.objects.get_or_create(user=user)
        context["settings"] = settings_obj

        return context    

def profile_update_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance = request.user)  # The instance=request.user binds the form to the logged-in user's instance, so it updates rather than creates.

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:  # If GET, load the current user data into the form.
        form = CustomUserChangeForm(instance =  request.user)
    return render(request, 'users/profile_update.html', {'form':form})

