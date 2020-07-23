from django.contrib import admin

from django_celery_beat.admin import (
    ClockedScheduleAdmin,
    PeriodicTaskAdmin,
)
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)

from django_otp.plugins.otp_static.admin import StaticDeviceAdmin
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django_otp.plugins.otp_totp.models import TOTPDevice

from otp_yubikey.admin import (
    RemoteYubikeyDeviceAdmin,
    ValidationServiceAdmin,
    YubikeyDeviceAdmin,
)
from otp_yubikey.models import (
    RemoteYubikeyDevice,
    ValidationService,
    YubikeyDevice,
)


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


class StaticDeviceStaffAdmin(VisibleToStaff, StaticDeviceAdmin):
    pass


class TOTPDeviceStaffAdmin(VisibleToStaff, TOTPDeviceAdmin):
    pass


# Register the Django OTP models
admin.site.register(StaticDevice, StaticDeviceAdmin)
admin.site.register(TOTPDevice, TOTPDeviceAdmin)
admin.site.register(YubikeyDevice, YubikeyDeviceAdmin)
admin.site.register(ValidationService, ValidationServiceAdmin)
admin.site.register(RemoteYubikeyDevice, RemoteYubikeyDeviceAdmin)

# Register the Django Celery Beat models
admin.site.register(PeriodicTask, PeriodicTaskAdmin)
admin.site.register(IntervalSchedule)
admin.site.register(CrontabSchedule)
admin.site.register(SolarSchedule)
admin.site.register(ClockedSchedule, ClockedScheduleAdmin)
