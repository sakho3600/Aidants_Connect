from django.contrib import admin
from django.contrib.auth.models import Group

from admin_honeypot.models import LoginAttempt
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from two_factor.models import PhoneDevice


class VisibleToStaff:
    """A mixin to make a model registered in the Admin visible to staff users."""

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)


# Unregister the Django Group model
admin.site.unregister(Group)

# Unregister the Honeypot model
admin.site.unregister(LoginAttempt)

# Unregister the Django Celery Beat models
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(SolarSchedule)
