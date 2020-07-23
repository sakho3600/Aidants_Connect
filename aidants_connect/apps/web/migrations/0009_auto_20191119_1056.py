# Generated by Django 2.2.4 on 2019-11-19 09:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("web", "0008_auto_20191021_1404")]

    operations = [
        migrations.RenameField(
            model_name="mandat",
            old_name="modified_by_access_token",
            new_name="last_mandat_renewal_token",
        ),
        migrations.AddField(
            model_name="mandat",
            name="expiration_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="mandat",
            name="last_mandat_renewal_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
