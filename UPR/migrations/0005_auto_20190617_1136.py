# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-06-17 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0004_auto_20190613_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentes',
            name='tipo_componentes',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
