from ..forms import SettingsForm
from ..models import UserSettings

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def settings_view(request):
    settings_object, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings_object)
        if form.is_valid():
            form.save()
            return redirect('user/profile')
    else:
        form = SettingsForm(instance=settings_object)
    return render(request, 'users/settings.html', {'form': form}) 

# (future) UserSettingsUpdateView
