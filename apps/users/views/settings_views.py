from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from ..models.user import UserSettings
from ..forms import SettingsForm

class UserSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = UserSettings 
    form_class = SettingsForm 
    template_name = 'users/settings_form.html'
    success_url = reverse_lazy('profile') # redirect after saving

    def get_object(self, queryset=None):
        # Ensure settings always exist for the logged-in user
        obj, created = UserSettings.objects.get_or_create(user=self.request.user)
        return obj