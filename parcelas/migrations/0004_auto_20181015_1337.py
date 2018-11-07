# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-10-15 11:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parcelas', '0003_auto_20181015_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parcela',
            name='propietario',
        ),
        migrations.AddField(
            model_name='parcela',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Propietario',
        ),
    ]