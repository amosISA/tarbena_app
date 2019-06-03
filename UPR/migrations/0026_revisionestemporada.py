# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-24 06:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0025_auto_20190523_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevisionesTemporada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('nombre_revision', models.CharField(blank=True, max_length=250, null=True)),
                ('fecha_revisión', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]