import pytz
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from .models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Username"),
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }


class ProfileForm(forms.ModelForm):
    TIME_ZONE_CHOICES = [('', '')] + [(t, t) for t in pytz.common_timezones]
    timezone = forms.ChoiceField(
        label=_("Timezone"),
        choices=TIME_ZONE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Profile
        fields = ('timezone',)