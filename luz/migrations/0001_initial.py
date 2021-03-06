# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-03-18 10:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=250, null=True)),
                ('codigo', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Contador',
                'verbose_name_plural': 'Contadores',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('desde', models.DateField(blank=True, null=True)),
                ('hasta', models.DateField(blank=True, null=True)),
                ('cantidad', models.CharField(blank=True, max_length=250, null=True)),
                ('lectura_anterior', models.CharField(blank=True, max_length=250, null=True)),
                ('lectura_posterior', models.CharField(blank=True, max_length=250, null=True)),
                ('consumo', models.CharField(blank=True, max_length=250, null=True)),
                ('contador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contadores', to='luz.Contador')),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
                'ordering': ['desde'],
            },
        ),
    ]
