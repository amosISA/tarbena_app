# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

class Provincia(TimeStampedModel):
    nombre = models.CharField(max_length=250, blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = 'Provincia'
        verbose_name_plural = "Provincias"

    def __str__(self):
        return '{}, {}'.format(self.codigo, self.nombre)

class Poblacion(TimeStampedModel):
    nombre = models.CharField(max_length=250, blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True, null=True)
    provincia = models.ForeignKey(Provincia, blank=True, null=True)
    dc = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ["codigo"]
        verbose_name = 'Poblacion'
        verbose_name_plural = "Poblaciones"

    def __str__(self):
        return '{}, {}'.format(self.codigo, self.nombre)

class Propietario(TimeStampedModel):
    nombre = models.CharField(max_length=250, blank=False)
    apellidos = models.CharField(max_length=250, blank=True)
    apellidos2 = models.CharField(max_length=250, blank=True)
    nif = models.CharField(max_length=250, blank=True, unique=True, help_text='Ejemplo: 12345678-T')
    poblacion = models.ForeignKey(Poblacion, blank=True, null=True, related_name='propietario_poblacion')
    direccion = models.CharField(max_length=250, blank=True)
    telefono_fijo = models.CharField(max_length=250, blank=True)
    telefono_movil = models.CharField(max_length=250, blank=True)
    email = models.CharField(max_length=250, blank=True)
    comentarios = models.TextField(blank=True)

    class Meta:
        ordering = ["-nombre"]
        verbose_name = 'Propietario'
        verbose_name_plural = "Propietarios"

    def __str__(self):
        return '{}, {} {}, {}, ({})'.format(self.nif ,self.apellidos, self.apellidos2, self.nombre, self.direccion)

    def natural_key(self):
        return '{}, {} {}, {}, ({})'.format(self.nif, self.apellidos, self.apellidos2, self.nombre, self.direccion)

class Estado(models.Model):
    nombre = models.CharField(max_length=250, blank=False)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return '{}'.format(self.nombre)

    def estado_nombre(self):
        return '{}'.format(self.nombre)

class SectorTrabajo(models.Model):
    sector = models.CharField(max_length=250, blank=False)

    class Meta:
        ordering = ["sector"]
        verbose_name = 'Sector Trabajo'
        verbose_name_plural = "Sectores de Trabajo"

    def __str__(self):
        return '{}'.format(self.sector)

class PoblacionesFavoritas(TimeStampedModel):
    user = models.ForeignKey(User, blank=True, null=True)
    poblacion = models.ManyToManyField(Poblacion, blank=True, related_name='poblacion')

    class Meta:
        ordering = ["user"]
        verbose_name = 'Poblaciones favoritas'
        verbose_name_plural = "Poblaciones favoritas"

    def __str__(self):
        return '{}'.format(self.user)

class Estado_Parcela_Trabajo(TimeStampedModel):
    nombre = models.CharField(max_length=250)
    porcentaje = models.CharField(max_length=250)

    class Meta:
        ordering = ["nombre"]
        verbose_name = 'Estado Parcela Trabajo'
        verbose_name_plural = "Estados Parcelas Trabajo"

    def __str__(self):
        return '{} ({})'.format(self.nombre, self.porcentaje)

class Parcela(TimeStampedModel):
    #user = models.ForeignKey(User, blank=True, null=True)
    propietario = models.ForeignKey(Propietario, related_name='propietario', default='', blank=True)
    poblacion = models.ForeignKey(Poblacion, default='')
    metros_cuadrados = models.CharField(max_length=250, blank=True)
    poligono = models.CharField(max_length=250)
    numero_parcela = models.CharField(max_length=250)
    estado = models.ForeignKey(Estado, related_name='estado', blank=True, null=True)
    estado_parcela_trabajo = models.ForeignKey(Estado_Parcela_Trabajo, blank=True, null=True, default=3)
    comentarios = models.TextField(blank=True)
    # https://stackoverflow.com/questions/35459326/foreignkey-to-a-model-that-is-defined-after-below-the-current-model?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    # nice help for use foreignkey for model that is below this one
    sector_trabajo = models.ManyToManyField(SectorTrabajo, blank=True)
    kml = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = 'Parcela'
        verbose_name_plural = "Parcelas"

    def __str__(self):
        return '{}'.format(self.numero_parcela)

class Proyecto(TimeStampedModel):
    nombre = models.CharField(max_length=250, blank=False)
    sector_trabajo = models.ManyToManyField(SectorTrabajo, blank=True)
    descripcion = models.TextField(blank=True)
    comentarios = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return '{}'.format(self.nombre)
