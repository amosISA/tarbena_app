# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-16 06:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0006_auto_20181016_0740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='propietario',
            old_name='calle',
            new_name='direccion',
        ),
    ]
