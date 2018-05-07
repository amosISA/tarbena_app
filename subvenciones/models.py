# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify

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

class Estado(TimeStampedModel):
    nombre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, default=None, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        ordering = ["nombre"]

    def save(self):
        self.slug = slugify(self.nombre)
        super(Estado, self).save()

    def get_absolute_url(self):
        return reverse('subvenciones:subvencion_by_category',
                       args=[self.slug])

    def count_subsidies(self):
        return Subvencion.objects.filter(estado=self.etapa)

class Colectivo(models.Model):
    nombre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, default=None, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        ordering = ["nombre"]

    def save(self):
        self.slug = slugify(self.nombre)
        super(Colectivo, self).save()

    def get_absolute_url(self):
        return reverse('subvenciones:subvencion_by_category',
                       args=[self.slug])

class Area(TimeStampedModel):
    nombre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, default=None, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        ordering = ['nombre',]

    def save(self):
        self.slug = slugify(self.nombre)
        super(Area, self).save()

    def get_absolute_url(self):
        return reverse('subvenciones:subvencion_by_category',
                       args=[self.slug])

class Ente(TimeStampedModel):
    nombre = models.CharField(max_length=250)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, default=None, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        ordering = ['nombre',]

    def save(self):
        self.slug = slugify(self.nombre)
        super(Ente, self).save()

    def get_absolute_url(self):
        return reverse('subvenciones:subvencion_by_category',
                       args=[self.slug])

class Subvencion(TimeStampedModel):
    user = models.ForeignKey(User, blank=True, null=True)
    inicio = models.DateField(blank=True, null=True)
    fin = models.DateField(blank=True, null=True)
    nombre = models.TextField(blank=False, default="")

    # Links
    procedimiento = models.TextField(blank=True)
    bases = models.TextField(blank=True)
    solicitud = models.TextField(blank=True)

    cuantia_inicial = models.CharField(max_length=250, blank=True, null=True)
    cuantia_final = models.CharField(max_length=250, blank=True, null=True)

    descripcion = models.TextField(blank=True)
    estado = models.ForeignKey(Estado)

    # Expediente
    drive = models.TextField(blank=True, null=True)
    gestiona_expediente = models.CharField(max_length=250, blank=True, null=True)
    nombre_carpeta_drive = models.TextField(blank=True, null=True)

    se_relaciona_con = models.ManyToManyField('self', blank=True, default='')
    colectivo = models.ManyToManyField(Colectivo, blank=True)

    ente = models.ForeignKey(Ente)

    likes = models.ManyToManyField(User, blank=True, related_name='subvencion_likes')

    class Meta:
        ordering = ["fin"]
        verbose_name = 'Subvencion'
        verbose_name_plural = "Subvenciones"

    def __str__(self):
        if self.fin == None:
            return '{}'.format(self.nombre)
        else:
            return '{} {}'.format(self.nombre, self.fin.strftime("%Y"))

    # def get_absolute_url(self):
    #     return reverse('myapp:subvencion_detail',
    #                    args=[self.id, self.slug])

class Comment(TimeStampedModel):
    user = models.ForeignKey(User)
    subvencion = models.ForeignKey(Subvencion, related_name='comments')
    contenido = models.TextField(blank=False, null=False, default='')
    active = models.BooleanField(default=True)  # field I use to deactivate inappropiate comments

    class Meta:
        ordering = ['-created',]

    def __str__(self):
        return 'Comentado por {}, {}'.format(self.user, self.subvencion)

class Like(TimeStampedModel):
    liked_by = models.ForeignKey(User)
    subvencion = models.ForeignKey(Subvencion)

    class Meta:
        ordering = ['-created',]
