# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-26 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subvenciones', '0017_auto_20180622_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='subvencion',
            name='fecha_resolucion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
