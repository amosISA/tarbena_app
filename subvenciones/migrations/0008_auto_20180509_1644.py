# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-09 14:44
from __future__ import unicode_literals

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('subvenciones', '0007_auto_20180509_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contenido',
            field=martor.models.MartorField(),
        ),
    ]
