# Generated by Django 3.0.5 on 2020-05-28 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("aidants_connect_web", "0023_rename_mandat_print"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="mandat",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]