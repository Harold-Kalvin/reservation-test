from django.contrib import admin

from reservation.models import ResourceType, Resource, Reservation
from reservation.forms import ReservationForm


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'localization', 'capacity')

class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm # for the clean method
    list_display = ('resource', 'from_date_time', 'to_date_time', 'owner')
    fields = ('resource', 'from_date_time', 'to_date_time')

    def save_model(self, request, obj, form, change):
        # save current user as owner if null
        if not obj.owner:
            obj.owner = request.user
        obj.save()

admin.site.register(ResourceType)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Reservation, ReservationAdmin)