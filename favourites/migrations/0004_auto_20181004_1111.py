# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-04 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('favourites', '0003_favourite_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favourite',
            name='group',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='favourite_group', to='auth.Group'),
        ),
    ]