from django.db import models

import os
import datetime

# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

class Classe(TimeStampedModel):
    nom = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nom)

    class Meta:
        ordering = ['nom',]

class Tipus(TimeStampedModel):
    nom = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nom)

    class Meta:
        ordering = ['nom',]

def upload_location(instance, filename):
    return os.path.join('museo/imatges/', datetime.datetime.now().date().strftime("%Y/%m/%d"), filename)

class Museo(TimeStampedModel):
    n_inventari = models.CharField(max_length=250, blank=True, null=True)
    nom = models.CharField(max_length=250, blank=True, null=True)
    imatge = models.ImageField(blank=True, null=True, upload_to=upload_location)
    classe = models.ForeignKey(Classe, blank=True, null=True, related_name='museo_classe')
    tipus = models.ForeignKey(Classe, blank=True, null=True, related_name='museo_tipus')
    n_peces = models.IntegerField(blank=True, null=True)
    utilitat = models.CharField(max_length=250, blank=True, null=True)
    procedencia = models.CharField(max_length=250, blank=True, null=True)
    exposada = models.BooleanField(default=False)
    propietari = models.CharField(max_length=250, blank=True, null=True)
    donacio = models.BooleanField(default=False)
    n_diposit_material = models.CharField(max_length=250, blank=True, null=True)
    descripcio_us = models.TextField(blank=True, null=True)
    mesura_llarg_alt = models.CharField(max_length=250, blank=True, null=True, help_text='En (cm)')
    mesura_ample = models.CharField(max_length=250, blank=True, null=True, help_text='En (cm)')
    mesura_grueso_fons = models.CharField(max_length=250, blank=True, null=True, help_text='En (cm)')
    mesura_diametre = models.CharField(max_length=250, blank=True, null=True, help_text='En (cm)')
    material_fabricacio = models.CharField(max_length=250, blank=True, null=True)
    tecnica_fabricacio = models.CharField(max_length=250, blank=True, null=True)
    any_fabricacio = models.CharField(max_length=250, blank=True, null=True)
    any_us = models.CharField(max_length=250, blank=True, null=True)
    restauracio = models.CharField(max_length=250, blank=True, null=True)
    estat_conservacio = models.CharField(max_length=250, blank=True, null=True)
    data_catalogacio = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nom)

    class Meta:
        ordering = ['nom',]