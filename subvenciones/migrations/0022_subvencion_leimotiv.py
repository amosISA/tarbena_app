# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-03 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subvenciones', '0021_auto_20180817_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='subvencion',
            name='leimotiv',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
