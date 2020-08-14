from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from . import forms as login_forms


User = get_user_model()

TEMPLATES_PATH = 'flexauth/login'


def login_username(request):
    form_class = login_forms.EmailUsernameForm

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():

            username = request.POST.get('username')
            first_factor = settings.FLEXAUTH_DEFAULT_1AF
            try:
                user = User.objects.get(username=username, is_active=True)
            except User.DoesNotExist:
                user = None
            else:
                first_factor = user.first_factor or first_factor
                if first_factor == 'email':
                    user.send_sesame()

            request.session['username'] = username
            return redirect(request.POST.get('next'))
    else:
        form = form_class()

    template_name = "%s/%s.html" % (TEMPLATES_PATH, 'username')
    return render(request, template_name, {
        'form': form,
        'next': 'flexauth:login_first_factor',
    })


def login_first_factor(request):
    username = request.session.get('username')
    if not username:
        return redirect('flexauth:login')

    first_factor = settings.FLEXAUTH_DEFAULT_1AF
    try:
        user = User.objects.get(username=username, is_active=True)
    except User.DoesNotExist:
        user = None
    else:
        first_factor = user.first_factor or first_factor

    form_class = login_forms.get_first_factor_login_form_class(first_factor)

    if request.method == 'POST':
        form = form_class(request.POST)
        if user and form.is_valid():
            if form.authenticate(request, username):

                if user.second_factor in ('sms', 'call'):
                    phone = user.phone_device
                    phone.generate_challenge()

                return redirect(request.POST.get('next'))
    else:
        form = form_class()

    template_name = "%s/%s_%s.html" % (
        TEMPLATES_PATH,
        'first_factor',
        first_factor,
    )
    return render(request, template_name, {
        'form': form,
        'prev': 'flexauth:login',
        'next': 'flexauth:login_second_factor',
    })


def login_second_factor(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('flexauth:login')

    second_factor = user.second_factor or settings.FLEXAUTH_DEFAULT_2AF
    form_class = login_forms.get_second_factor_login_form_class(second_factor)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            if form.authenticate(request):
                return redirect(request.POST.get('next'))
    else:
        form = form_class()

    template_name = "%s/%s_%s.html" % (
        TEMPLATES_PATH,
        'second_factor',
        second_factor,
    )
    return render(request, template_name, {
        'form': form,
        'prev': 'flexauth:login_first_factor',
        'next': settings.LOGIN_REDIRECT_URL,
    })
