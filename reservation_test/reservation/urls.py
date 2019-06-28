from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.home), name="home"),
    path('reserve/', login_required(views.ReservationCreateView.as_view()), name="reservation-add"),
    path('<int:pk>/update/', login_required(views.ReservationUpdateView.as_view()), name='reservation-update'),
    path('<int:pk>/remove/', login_required(views.remove_reservation), name='reservation-remove'),
]
