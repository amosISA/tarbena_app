# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-16 15:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0018_remove_incidencias_funcionamiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencias',
            name='operativo',
            field=models.BooleanField(default=True),
        ),
    ]