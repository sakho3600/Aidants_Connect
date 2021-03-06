# Generated by Django 3.0.3 on 2020-02-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aidants_connect_web", "0017_journal_action_add_franceconnection_usager"),
    ]

    operations = [
        migrations.AddField(
            model_name="journal",
            name="mandat_print_hash",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="journal",
            name="action",
            field=models.CharField(
                choices=[
                    ("connect_aidant", "Connexion d'un aidant"),
                    ("activity_check_aidant", "Reprise de connexion d'un aidant"),
                    ("franceconnect_usager", "FranceConnexion d'un usager"),
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
