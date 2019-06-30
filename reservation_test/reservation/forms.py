from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        exclude = ('owner',)
        widgets = {
            'resource': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        resource = self.cleaned_data.get('resource')
        start = self.cleaned_data.get('from_date_time')
        end = self.cleaned_data.get('to_date_time')
        
        # prevents from creating a "start date time" greater than "end date time"
        if end < start:
            raise ValidationError({'to_date_time': [
                _("'To date time' must be greater than 'from date time'.")
            ]})

        # prevents from creating a "start date time" greater than the current time
        if end < timezone.now():
            raise ValidationError({'to_date_time': [
                _("'To date time' must be greater than the current time.")
            ]})
        
        # prevents from creating a reservation if the "start" or "end" is within 
        # the time range of another reservation of the same resource
        # TODO: exclude the current object in this condition
        blocking_reservations = Reservation.objects.filter(resource=resource).filter(
            Q(from_date_time__lt=start, to_date_time__gt=start) |
            Q(from_date_time__lt=end, to_date_time__gt=end, )
        )
        if blocking_reservations:
            raise ValidationError({'resource': [
                _("This resource is already reserved for this time range.")
            ]})

        # TODO: a user cannot be at two places at the same time