
import math
from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.template import loader
from django.urls import reverse

from django_otp.plugins.otp_totp.models import TOTPDevice
from otp_yubikey.models import RemoteYubikeyDevice
from two_factor.models import PhoneDevice

from . import constants
from .login.forms import (
    get_first_factor_login_form_class,
    get_second_factor_login_form_class,
)


class WithFlexAuth(models.Model):
    has_completed_registration = models.BooleanField(
        "a terminé son inscription",
        default=False,
    )
    first_factor = models.CharField(
        "préfère se connecter",
        max_length=8,
        blank=True,
        choices=constants.FirstFactor.choices,
    )
    second_factor = models.CharField(
        "confirme son identité",
        max_length=8,
        blank=True,
        choices=constants.SecondFactor.choices,
    )

    class Meta:
        abstract = True

    @property
    def first_factor_login_form_class(self):
        return get_first_factor_login_form_class(self.first_factor)

    @property
    def second_factor_login_form_class(self):
        return get_second_factor_login_form_class(self.second_factor)

    @property
    def phone_device(self):
        return PhoneDevice.objects.filter(user=self).first()

    @property
    def totp_device(self):
        return TOTPDevice.objects.filter(user=self).first()

    @property
    def yubikey_device(self):
        return RemoteYubikeyDevice.objects.filter(user=self).first()

    @property
    def tfa_device(self):
        if self.second_factor in ('sms', 'call'):
            return self.phone_device
        elif self.second_factor == 'app':
            return self.totp_device
        elif self.second_factor == 'key':
            return self.yubikey_device

    def send_sesame(self, base_url=None, extra_params=None, extra_context=None):

        # Imported here because it triggers a premature
        # import of the custom auth model otherwise...
        from sesame.utils import get_parameters as get_sesame_params

        base_url = base_url or settings.FLEXAUTH_BASE_URL
        qs_params = get_sesame_params(self)
        if extra_params:
            qs_params.update(extra_params)

        sesame_url = '%s%s?%s' % (
            base_url,
            reverse('flexauth:login_second_factor'),  # TODO: try to omit namespace?
            urlencode(qs_params),
        )
        sesame_ttl_minutes = math.floor(settings.SESAME_MAX_AGE / 60)

        TEMPLATES_PATH = 'flexauth/email'
        subject_template = '%s/subject.txt' % TEMPLATES_PATH
        text_body_template = '%s/body.txt' % TEMPLATES_PATH
        html_body_template = '%s/body.html' % TEMPLATES_PATH

        context = {
            'user': self,
            'sesame_url': sesame_url,
            'sesame_ttl_minutes': sesame_ttl_minutes,
        }
        if extra_context:
            context.update(extra_context)

        subject = loader.render_to_string(subject_template, context).rstrip()
        text_body = loader.render_to_string(text_body_template, context)
        html_body = loader.render_to_string(html_body_template, context)
        send_mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            subject=subject,
            message=text_body,
            html_message=html_body,
            recipient_list=[self.email],
            fail_silently=False,
        )
