from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker_plus import DateTimePickerInput

from reservation.models import Reservation
from reservation.forms import ReservationForm
from reservation.utils import past_reservations, current_reservations, coming_reservations


def home(request):
    """
    Home page which contains the list of all the past, current and
    coming reservations.
    """    
    past = past_reservations(request)
    current = current_reservations(request)
    coming = coming_reservations(request)

    return render(request, 'reservation/home.html', {
        'past_reservations': past,
        'current_reservations': current,
        'coming_reservations': coming,
    })


class AjaxableResponseMixin:
    """Mixin to add AJAX support to a form."""
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            form.errors['message'] = _("Reservation was not successful. See errors below.")
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {'message': _("Reservation was successful.")}
            return JsonResponse(data)
        else:
            return response


class ReservationCreateView(AjaxableResponseMixin, CreateView):
    """Generic view for the 'create reservation' page."""
    model = Reservation
    template_name = 'reservation/reserve_form.html'
    form_class = ReservationForm
    success_url = reverse_lazy('home')

    def get_form(self):
        form = super().get_form()
        # use a bootstrap date time picker for some fields
        form.fields['from_date_time'].widget = DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"},
        )
        form.fields['to_date_time'].widget = DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"},
        )
        return form

    def form_valid(self, form):
        # saving current user as owner
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super(ReservationCreateView, self).form_valid(form)


class ReservationUpdateView(AjaxableResponseMixin, UpdateView):
    """Generic view for the 'update reservation' page."""
    model = Reservation
    template_name = 'reservation/reserve_form.html'
    form_class = ReservationForm
    success_url = reverse_lazy('home')

    def get_form(self):
        form = super().get_form()
        # use a bootstrap date time picker for some fields
        form.fields['from_date_time'].widget = DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"},
        )
        form.fields['to_date_time'].widget = DateTimePickerInput(
            options={"format": "YYYY-MM-DD HH:mm"},
        )
        return form

    def get_context_data(self, **kwargs):
        data = super(ReservationUpdateView, self).get_context_data(**kwargs)
        # if reservation has passed, raise 404 error 
        if not self.object.is_coming():
            raise Http404()
        return data

    def form_valid(self, form):
        # saving current user as owner if needed
        self.object = form.save(commit=False)
        if not self.object.owner:
            self.object.owner = self.request.user
        self.object.save()
        return super(ReservationUpdateView, self).form_valid(form)


def remove_reservation(request, pk):
    """Removes a reservation and sends a response back to an ajax call."""
    if request.method == 'POST':
        to_remove = Reservation.objects.get(id=pk)
        is_current = to_remove.is_current()
        is_coming = to_remove.is_coming()
        
        # finally removes entry
        to_remove.delete()

        html = None
        if is_current:
            current = current_reservations(request)
            # create html to send as response
            html = render_to_string(
                'reservation/sub_templates/current_reservation_items.html', {
                    'current_reservations': current,
                }
            )
        elif is_coming:
            coming = coming_reservations(request)
            # create html to send as response
            html = render_to_string(
                'reservation/sub_templates/coming_reservation_items.html', {
                    'coming_reservations': coming,
                }
            )

        data = {'html': html, 'is_current': is_current, 'is_coming': is_coming}
        return JsonResponse(data)
    else:
        raise Http404()
