# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-09 11:21
from __future__ import unicode_literals

import UPR.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0006_auto_20190509_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentes',
            name='imatge_componente',
            field=models.ImageField(null=True, upload_to=UPR.models.upload_location),
        ),
        migrations.AddField(
            model_name='componentes',
            name='tipo_comentario',
            field=models.TextField(blank=True, null=True),
        ),
    ]