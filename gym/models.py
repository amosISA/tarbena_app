from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

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

class Gym(TimeStampedModel):
    user = models.ForeignKey(User, blank=True, null=True)
    edad = models.CharField(max_length=250, blank=True, null=True)
    vigencia = models.CharField(max_length=250, blank=True, null=True)
    cuantia = models.CharField(max_length=250, blank=True, null=True)
    fecha_pagado = models.DateField(blank=True, null=True)
    valido_hasta = models.DateField(blank=True, null=True)
    pagado = models.BooleanField(default=False)

    def __str__(self):
        return self.user