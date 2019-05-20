# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-16 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0012_poblacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comarca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(blank=True, max_length=250, null=True)),
                ('codigo', models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
                'ordering': ['nombre'],
            },
        ),
        migrations.AlterModelOptions(
            name='poblacion',
            options={'ordering': ['codigo_INE'], 'verbose_name': 'Poblacion', 'verbose_name_plural': 'Poblaciones'},
        ),
        migrations.RenameField(
            model_name='poblacion',
            old_name='codigo',
            new_name='codigo_INE',
        ),
        migrations.RemoveField(
            model_name='poblacion',
            name='dc',
        ),
        migrations.AddField(
            model_name='poblacion',
            name='orden_noel',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='poblacion',
            name='comarca',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UPR.Comarca'),
        ),
        migrations.AddField(
            model_name='poblacion',
            name='provincia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UPR.Provincia'),
        ),
    ]