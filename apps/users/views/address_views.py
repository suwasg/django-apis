from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import *
from ..forms import  AddressForm

# for CBVs
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

@login_required
def add_address_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST) # If form is submitted, populate with POST data.

        if form.is_valid():
            address = form.save(commit = False) # If valid, create an address object but don’t save it yet (commit=False). You do this because you still need to assign the user.
            address.user =  request.user # Attach the currently logged-in user to the address.
            address.save() # Save the address.
            messages.success(request, "Address Added successfully.")
            return redirect('profile') # Redirect to the profile page.

    else: # For GET request, create an empty address form.
        form = AddressForm()
    return render(request, 'users/add_address.html', {'form':form})

class AddressListView(LoginRequiredMixin, ListView):
    model = Address 
    template_name = 'users/address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        # only return the addresses for the logged in users.
        return Address.objects.filter(user= self.request.user)

class AddressDetailView(LoginRequiredMixin, DetailView):
    model = Address
    template_name = 'users/address_detail.html'
    context_object_name = 'address'

    def test_func(self):
        # only owner can view details
        return self.get_object().user == self.request.user

class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm 
    template_name = 'users/address_form.html'
    success_url = reverse_lazy('address_list')

    def form_valid(self, form):
        form.instance.user = self.request.user # assign the owner/user
        messages.success(self.request, "Address Added successfully using CBV.")
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "users/address_form.html"
    success_url = reverse_lazy("address_list")

    def test_func(self):
        # Only owner can update
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Address updated successfully.")
        return super().form_valid(form)

class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Address
    template_name = "users/address_confirm_delete.html"
    success_url = reverse_lazy("address_list")

    def test_func(self):
        # Only owner can delete
        return self.get_object().user == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Address deleted successfully.")
        return super().delete(request, *args, **kwargs)