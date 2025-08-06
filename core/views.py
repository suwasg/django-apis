from django.shortcuts import render
from django.http import HttpResponse
from django.views .generic import ListView, CreateView,DetailView,UpdateView,DeleteView

# Create your views here.
# 2 -> FBV,CBV (function base views, )

#Function Base Views
def homepage_view(request):
    return render(request, 'home.html')