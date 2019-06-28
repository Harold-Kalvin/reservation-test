from django.db import models
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class ResourceType(models.Model):
    """Model for resource types which defines a resource."""
    name = models.CharField(_("Name"), max_length=256)

    class Meta:
        verbose_name = _("Resource type")
        verbose_name_plural = _("Resource types")
    
    def __str__(self):
        return self.name


class Resource(models.Model):
    """Model for resources which can be reserved."""
    name = models.CharField(_("Name"), max_length=256)
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    localization = models.CharField(_("Localization"), max_length=256)
    capacity = models.PositiveSmallIntegerField(
        _("Capacity"),
        default=1,
        validators=[MinValueValidator(1, message=_("The minimum value is 1."))]
    )

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
    
    def __str__(self):
        return self.name


class Reservation(models.Model):
    """Model for reservations."""
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    from_date_time = models.DateTimeField(_("From"), default=timezone.now)
    to_date_time = models.DateTimeField(_("To"))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            null=True)

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        # to show the datetimes in the current timezone 
        tz = get_current_timezone()
        return _("""Reservation of "%(res)s" (%(from)s => %(to)s)""") % {
            "res": self.resource,
            "from": self.from_date_time.astimezone(tz).strftime("%Y/%m/%d %H:%S"),
            "to": self.to_date_time.astimezone(tz).strftime("%Y/%m/%d %H:%S"),
        }

    def is_past(self):
        now = timezone.now()
        return self.from_date_time < now and self.to_date_time < now

    def is_current(self):
        now = timezone.now()
        return self.from_date_time <= now and self.to_date_time >= now

    def is_coming(self):
        now = timezone.now()
        return self.from_date_time > now and self.to_date_time > now