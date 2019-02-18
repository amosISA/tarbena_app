# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-18 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import museo.models


class Migration(migrations.Migration):

    dependencies = [
        ('museo', '0004_auto_20190215_0730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imatge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('imatge', models.ImageField(upload_to=museo.models.upload_location)),
                ('position', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.RemoveField(
            model_name='museo',
            name='imatge',
        ),
        migrations.AddField(
            model_name='imatge',
            name='museo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagtges', to='museo.Museo'),
        ),
    ]
