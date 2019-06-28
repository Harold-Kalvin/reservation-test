from django.utils import timezone

import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.profile.timezone:
                timezone.activate(pytz.timezone(request.user.profile.timezone))

        response = self.get_response(request)
        return response
