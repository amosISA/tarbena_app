# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-04 07:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('favourites', '0002_auto_20180924_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='favourite',
            name='group',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='favourite_group', to='auth.Group'),
            preserve_default=False,
        ),
    ]
