# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-12-07 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_auto_20181207_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractor',
            name='pagina_web',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
