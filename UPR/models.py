from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

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

def upload_location(instance, filename):
    return os.path.join('UPR/img/', datetime.datetime.now().date().strftime("%Y/%m/%d"), filename)

class TipoMaquina(TimeStampedModel):
    tipo = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.tipo)

class Componentes(TimeStampedModel):
    tipo_componentes = models.CharField(max_length=250, blank=True, null=True)
    tipo_comentario = models.TextField(blank=True, null=True)
    imatge_componente = models.ImageField(upload_to=upload_location, null=True, blank=True)
    tipo_maquina = models.ManyToManyField(TipoMaquina, blank=True, related_name='tipo_maquina_componente')

    def __str__(self):
        return '{}'.format(self.tipo_componentes)

    class Meta:
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'

class Incidencias(TimeStampedModel):
    tipo_incidencias = models.ForeignKey(Componentes, blank=True, null=True, related_name='tipo_componente')
    fecha = models.DateField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.tipo_incidencias)

    class Meta:
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'

class Maquina(TimeStampedModel):
    numero_inventario = models.CharField(max_length=250, blank=True, null=True)
    numero_serie = models.CharField(max_length=250, blank=True, null=True)
    fecha_compra = models.DateField(blank=True, null=True)
    tipo_maquina = models.ForeignKey(TipoMaquina, blank=True, null=True, related_name='tipo_maquinas')
    incidencias = models.ManyToManyField(Incidencias, blank=True, related_name='tipo_incidencia')
    capataz_responsable = models.ForeignKey(User, blank=True, null=True,)

    def __str__(self):
        return '{}'.format(self.numero_inventario)