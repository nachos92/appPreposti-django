# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Segnalazione',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('dettaglio', models.TextField(max_length=200, blank=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'segnalazioni (dipendenti)',
            },
        ),
        migrations.CreateModel(
            name='SegnalazionePrep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('dettaglio', models.TextField(max_length=200, blank=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'segnalazioni (preposti)',
            },
        ),
        migrations.CreateModel(
            name='Settimana',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creazione', models.DateTimeField(auto_now_add=True)),
                ('data_inizio', models.DateField(help_text=b"Deve essere un lunedi'.")),
                ('lun_fatto', models.BooleanField(default=False)),
                ('mar_fatto', models.BooleanField(default=False)),
                ('mer_fatto', models.BooleanField(default=False)),
                ('gio_fatto', models.BooleanField(default=False)),
                ('ven_fatto', models.BooleanField(default=False)),
                ('lun_check', models.BooleanField(default=False)),
                ('mar_check', models.BooleanField(default=False)),
                ('mer_check', models.BooleanField(default=False)),
                ('gio_check', models.BooleanField(default=False)),
                ('ven_check', models.BooleanField(default=False)),
                ('completato', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'Planning settimanali',
            },
        ),
    ]
