# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-20 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0020_auto_20190517_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentes',
            name='tipo_opciones',
            field=models.TextField(blank=True, null=True),
        ),
    ]
