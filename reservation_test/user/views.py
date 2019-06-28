from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .models import Profile
from .forms import UserForm, ProfileForm


@transaction.atomic
def update_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        # if both user and profile forms are valid, save both 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Profile successfully updated.'))
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the errors.'))

    return render (request, 'user/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })