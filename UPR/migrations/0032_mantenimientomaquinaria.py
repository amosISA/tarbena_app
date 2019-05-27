# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-05-27 09:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UPR', '0031_auto_20190527_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='MantenimientoMaquinaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('nombre_revision', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nombreRevision', to='UPR.RevisionesTemporada')),
                ('numero_incidencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='numeroIncidencia', to='UPR.Incidencias')),
                ('numero_maquina', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='numeroMaquina', to='UPR.Maquina')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
