# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-16 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0014_auto_20190516_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poblacion',
            name='provincia',
        ),
        migrations.AddField(
            model_name='maquina',
            name='maquina_poblacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nombre_poblacion', to='UPR.Poblacion'),
        ),
    ]