from django.urls import path
from apps.users import views
# cbvs
from apps.users.views import (
    AddressCreateView, 
    AddressDetailView, 
    AddressListView, 
    AddressUpdateView, 
    AddressDeleteView, 
    register_view,
    login_view,
    logout_view,
    profile_view,
    profile_update_view,
    deactivate_account_view,
    delete_account_view,
    ProfileView,
    UserSettingsUpdateView,
    )

urlpatterns = [
    # Auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Profile
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", views.profile_update_view, name="profile_update"),

    # Addresses
    # path("addresses/add/", views.add_address_view, name="add_address"),
     path("addresses/", AddressListView.as_view(), name="address_list"),
    path("addresses/<int:pk>/", AddressDetailView.as_view(), name="address_detail"),
    path("addresses/add/", AddressCreateView.as_view(), name="address_add"),
    path("addresses/update/<int:pk>", AddressUpdateView.as_view(), name="address_edit"),
    path("addresses/<int:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"),


    # Account
    path("account/deactivate/", views.deactivate_account_view, name="account_deactivate"),
    path("account/delete/", views.delete_account_view, name="account_delete"),

    # Settings
    path("settings/update/", UserSettingsUpdateView.as_view() , name="settings_update"),
]
