# Generated by Django 3.0.3 on 2020-04-01 13:18

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aidants_connect_web', '0020_journal_action_add_update_email_usager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autorisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('demarche', models.CharField(choices=[('papiers', 'Papiers - Citoyenneté'), ('famille', 'Famille'), ('social', 'Social - Santé'), ('travail', 'Travail'), ('logement', 'Logement'), ('transports', 'Transports'), ('argent', 'Argent'), ('justice', 'Justice'), ('etranger', 'Étranger'), ('loisirs', 'Loisirs')], max_length=16)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expiration_date', models.DateTimeField()),
                ('last_usage_date', models.DateTimeField(blank=True, null=True)),
                ('mandat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autorisations', to='aidants_connect_web.Mandat')),
            ],
        ),
        migrations.CreateModel(
            name='Attestation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('creation', 'Création'), ('creation', 'Résiliation')], default='creation', max_length=16)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='')),
                ('mandat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attestations', to='aidants_connect_web.Mandat')),
            ],
        ),
        migrations.AddField(
            model_name='mandat',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='mandats', to='aidants_connect_web.Organisation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mandat',
            name='usager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mandats', to='aidants_connect_web.Usager'),
        ),
        migrations.AlterField(
            model_name='mandat',
            name='expiration_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterUniqueTogether(
            name='mandat',
            unique_together=set(),
        ),
    ]
