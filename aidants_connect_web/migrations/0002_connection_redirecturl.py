# Generated by Django 2.2 on 2019-06-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidants_connect_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='redirectUrl',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
