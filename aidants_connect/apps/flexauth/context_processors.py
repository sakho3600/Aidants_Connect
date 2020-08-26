from django.conf import settings


def registration_mode(request):
    return {'registration_mode': settings.FLEXAUTH_REGISTRATION_MODE}
