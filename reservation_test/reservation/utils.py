from django.utils import timezone

from reservation.models import Reservation


def past_reservations(request):
    """Returns a queryset of reservations thar are done."""
    past_reservations = Reservation.objects.filter(
        from_date_time__lt=timezone.now(), to_date_time__lt=timezone.now()
    ).select_related('resource__resource_type', 'owner')

    # unless admin, a user can only see his own reservations
    if not request.user.is_staff and not request.user.is_superuser:
        past_reservations = past_reservations.filter(owner=request.user)
    
    return past_reservations

    
def current_reservations(request):
    """Returns a queryset of reservations that are ongoing."""
    current_reservations = Reservation.objects.filter(
        from_date_time__lte=timezone.now(), to_date_time__gte=timezone.now()
    ).select_related('resource__resource_type', 'owner')

    # unless admin, a user can only see his own reservations
    if not request.user.is_staff and not request.user.is_superuser:
        current_reservations = current_reservations.filter(owner=request.user)
    
    return current_reservations


def coming_reservations(request):
    """Returns a queryset of reservations that have not started yet."""
    coming_reservations = Reservation.objects.filter(
        from_date_time__gt=timezone.now(), to_date_time__gt=timezone.now()
    ).select_related('resource__resource_type', 'owner')

    # unless admin, a user can only see his own reservations
    if not request.user.is_staff and not request.user.is_superuser:
        coming_reservations = coming_reservations.filter(owner=request.user)
    
    return coming_reservations