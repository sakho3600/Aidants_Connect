import logging

from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from django_otp.decorators import otp_required

from aidants_connect.apps.logs.models import Journal


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


@otp_required
@login_required
def dashboard(request):
    aidant = request.user
    messages = django_messages.get_messages(request)
    return render(
        request,
        "aidants/dashboard.html",
        {"aidant": aidant, "messages": messages},
    )


@otp_required
@login_required
def usagers_index(request):
    messages = django_messages.get_messages(request)
    aidant = request.user
    usagers = aidant.get_usagers()

    return render(
        request,
        "aidants/usagers.html",
        {"aidant": aidant, "usagers": usagers, "messages": messages},
    )


@otp_required
@login_required
def usager_details(request, usager_id):
    messages = django_messages.get_messages(request)
    aidant = request.user

    usager = aidant.get_usager(usager_id)
    if not usager:
        django_messages.error(request, "Cet usager est introuvable ou inaccessible.")
        return redirect("dashboard")

    active_autorisations = aidant.get_active_autorisations_for_usager(usager_id)
    inactive_autorisations = aidant.get_inactive_autorisations_for_usager(usager_id)

    return render(
        request,
        "aidants/usager_details.html",
        {
            "aidant": aidant,
            "usager": usager,
            "active_autorisations": active_autorisations,
            "inactive_autorisations": inactive_autorisations,
            "messages": messages,
        },
    )


@otp_required
@login_required
def usagers_mandats_autorisations_cancel_confirm(
    request, usager_id, mandat_id, autorisation_id
):
    aidant = request.user

    usager = aidant.get_usager(usager_id)
    if not usager:
        django_messages.error(request, "Cet usager est introuvable ou inaccessible.")
        return redirect("dashboard")

    autorisation = usager.get_autorisation(mandat_id, autorisation_id)
    if not autorisation:
        django_messages.error(
            request, "Cette autorisation est introuvable ou inaccessible."
        )
        return redirect("dashboard")
    if autorisation.is_revoked:
        django_messages.error(request, "L'autorisation a été révoquée")
        return redirect("dashboard")
    if autorisation.is_expired:
        django_messages.error(request, "L'autorisation a déjà expiré")
        return redirect("dashboard")

    if request.method == "POST":
        form = request.POST

        if form:
            autorisation.revocation_date = timezone.now()
            autorisation.save(update_fields=["revocation_date"])

            Journal.log_autorisation_cancel(autorisation, aidant)

            django_messages.success(
                request, "L'autorisation a été révoquée avec succès !"
            )
            return redirect("usager_details", usager_id=usager.id)

        else:
            return render(
                request,
                "aidants/usagers_mandats_autorisations_cancel_confirm.html",
                {
                    "aidant": aidant,
                    "usager": usager,
                    "autorisation": autorisation,
                    "error": "Erreur lors de l'annulation de l'autorisation.",
                },
            )

    return render(
        request,
        "aidants/usagers_mandats_autorisations_cancel_confirm.html",
        {"aidant": aidant, "usager": usager, "autorisation": autorisation},
    )
