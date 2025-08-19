from .account_views import deactivate_account_view, delete_account_view
from .address_views import (AddressListView, AddressDetailView, AddressCreateView, AddressUpdateView, AddressDeleteView)
from .auth_views import register_view, login_view, logout_view
from .profile_views import profile_view, profile_update_view
from .settings_views import UserSettingsUpdateView