# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-12-17 07:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcelas', '0007_auto_20181016_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado_Parcela_Trabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=250)),
                ('porcentaje', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Estado Parcela Trabajo',
                'verbose_name_plural': 'Estados Parcelas Trabajo',
                'ordering': ['nombre'],
            },
        ),
    ]
