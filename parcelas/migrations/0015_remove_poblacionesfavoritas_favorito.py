# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-16 07:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0014_auto_20190116_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poblacionesfavoritas',
            name='favorito',
        ),
    ]
