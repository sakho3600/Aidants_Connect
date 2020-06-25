# Generated by Django 3.0.5 on 2020-05-28 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidants_connect_web', '0023_connection_mandat_is_remote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journal',
            old_name='mandat_print_hash',
            new_name='attestation_hash',
        ),
        migrations.AlterField(
            model_name='journal',
            name='action',
            field=models.CharField(choices=[
                ('connect_aidant', "Connexion d'un aidant"),
                ('activity_check_aidant', "Reprise de connexion d'un aidant"),
                ('franceconnect_usager', "FranceConnexion d'un usager"),
                ('update_email_usager', "L'email de l'usager a été modifié"),
                ('create_attestation', "Création d'une attestation"),
                ('create_mandat', "Création d'un mandat"),
                ('use_mandat', "Utilisation d'un mandat"),
                ('update_mandat', "Renouvellement d'un mandat"),
                ('cancel_mandat', "Révocation d'un mandat")
            ], max_length=30),
        ),
    ]
