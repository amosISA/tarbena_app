# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-06-17 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0005_auto_20190617_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentes',
            name='tipo_componentes',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
