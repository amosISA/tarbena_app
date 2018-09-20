# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import model_to_dict
from django.template.defaultfilters import slugify

from martor.models import MartorField
from smart_selects.db_fields import ChainedForeignKey
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

class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    # https://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed

    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])

class Estado(TimeStampedModel):
    nombre = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, default=None, blank=True, null=True)
    color = models.CharField(max_length=250 ,default="#fff")

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
        return Subvencion.objects.select_related('estado').filter(estado=self.id)

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

class Ente(TimeStampedModel):
    nombre = models.CharField(max_length=250)
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

class Area(TimeStampedModel):
    nombre = models.CharField(max_length=250)
    ente = models.ForeignKey(Ente, on_delete=models.CASCADE, null=True)
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

class Subvencion(TimeStampedModel, ModelDiffMixin):
    user = models.ForeignKey(User, blank=True, null=True)
    fecha_publicacion = models.DateField(blank=True, null=True)
    fin = models.DateField(blank=True, null=True)
    fecha_resolucion = models.DateField(blank=True, null=True)
    responsable = models.ManyToManyField(User, related_name='responsable', blank=True)
    nombre = models.TextField(blank=False, default="")
    leimotiv = models.CharField(max_length=250, blank=True, null=True)

    # Links
    procedimiento = models.TextField(blank=True)
    bases = models.TextField(blank=True)
    solicitud = models.TextField(blank=True)

    cuantia_inicial = models.CharField(max_length=250, blank=True, null=True)
    cuantia_solicitada = models.CharField(max_length=250, blank=True, null=True)
    cuantia_final = models.CharField(max_length=250, blank=True, null=True)

    descripcion = models.TextField(blank=True)
    estado = models.ForeignKey(Estado)

    # Expediente
    drive = models.TextField(blank=True, null=True)
    gestiona_expediente = models.CharField(max_length=250, blank=True, null=True)
    nombre_carpeta_drive = models.TextField(blank=True, null=True)

    # Impreso o no
    impreso = models.BooleanField(default=False)

    se_relaciona_con = models.ManyToManyField('self', blank=True, default='')
    colectivo = models.ManyToManyField(Colectivo, blank=True)

    ente = models.ForeignKey(Ente, null=True)
    area = ChainedForeignKey(
        Area,
        chained_field="ente",
        chained_model_field="ente",
        show_all=False,
        auto_choose=True,
        sort=True,
        default=''
    )

    likes = models.ManyToManyField(User, blank=True, related_name='subvencion_likes')

    # Fechas Ejecución
    incio_ejecucion = models.DateField(blank=True, null=True)
    fin_ejecucion = models.DateField(blank=True, null=True)

    # Fechas Justificación
    fin_justificacion = models.DateField(blank=True, null=True)
    explicacion_justificacion = models.TextField(blank=True)

    class Meta:
        ordering = ["fin"]
        verbose_name = 'Subvencion'
        verbose_name_plural = "Subvenciones"

    def __str__(self):
        if self.fin == None:
            return '{}'.format(self.nombre)
        else:
            return '{} {}'.format(self.nombre, self.fin.strftime("%Y"))

    def get_absolute_url(self):
        return reverse('subvenciones:subvencion_detail',
                       args=[self.id])

    def get_sub_comments(self):
        return self.comments.all().select_related('user', 'subvencion')

class Comment(TimeStampedModel):
    user = models.ForeignKey(User, blank=True, null=True)
    subvencion = models.ForeignKey(Subvencion, related_name='comments')
    contenido = MartorField(blank=True)
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
