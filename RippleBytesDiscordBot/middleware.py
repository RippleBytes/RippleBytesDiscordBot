from django.utils.timezone import activate, deactivate
from pytz import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Fetch user's timezone, e.g., from the user profile
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and hasattr(user, 'timezone'):
            activate(timezone(user.timezone))  # Use user's timezone
        else:
            deactivate()  # Fallback to UTC

        response = self.get_response(request)
        return response
