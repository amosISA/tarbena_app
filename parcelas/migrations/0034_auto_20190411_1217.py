# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-04-11 10:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0033_auto_20190411_0857'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parcela',
            options={'ordering': ['propietario', 'poligono'], 'permissions': (('acceder_parcelas', 'Puede acceder a la app de parcelas'),), 'verbose_name': 'Parcela', 'verbose_name_plural': 'Parcelas'},
        ),
    ]