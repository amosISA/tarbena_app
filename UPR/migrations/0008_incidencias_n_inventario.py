# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-07-05 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0007_auto_20190704_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencias',
            name='n_inventario',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]