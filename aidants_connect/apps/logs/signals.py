from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Journal


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    Journal.log_connection(user)
