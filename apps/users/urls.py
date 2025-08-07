from django.urls import path
from .views import register_view, login_view, profile_view, profile_update_view

urlpatterns=[
   
    path('register', register_view, name = 'register'),
    path('login',login_view, name='login' ),
    path('profile', profile_view, name = 'profile'),
    path('update', profile_update_view, name = 'profile_update'),
]