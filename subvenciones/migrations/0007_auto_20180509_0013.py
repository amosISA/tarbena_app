# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-08 22:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subvenciones', '0006_auto_20180509_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ente',
            name='area',
        ),
        migrations.AddField(
            model_name='area',
            name='ente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subvenciones.Ente'),
        ),
    ]