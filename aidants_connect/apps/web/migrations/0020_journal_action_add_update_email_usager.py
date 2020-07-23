# Generated by Django 3.0.4 on 2020-03-12 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0019_normalize_usager_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journal",
            name="action",
            field=models.CharField(
                choices=[
                    ("connect_aidant", "Connexion d'un aidant"),
                    ("activity_check_aidant", "Reprise de connexion d'un aidant"),
                    ("franceconnect_usager", "FranceConnexion d'un usager"),
                    ("update_email_usager", "L'email de l'usager a été modifié"),
                    ("create_mandat_print", "Création d'un mandat papier"),
                    ("create_mandat", "Création d'un mandat"),
                    ("use_mandat", "Utilisation d'un mandat"),
                    ("update_mandat", "Renouvellement d'un mandat"),
                    ("cancel_mandat", "Révocation d'un mandat"),
                ],
                max_length=30,
            ),
        ),
    ]
