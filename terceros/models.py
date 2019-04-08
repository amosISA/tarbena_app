from django.db import models

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

class Terceros(TimeStampedModel):
    identificacion = models.CharField(max_length=255, unique=True, blank=True, null=True, help_text='NIF/CIF/Otro/Ninguna')
    nombre = models.CharField(max_length=255)
    primer_apellido = models.CharField(max_length=255, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=255, blank=True, null=True)
    movil = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    pagina_web = models.CharField(max_length=255, blank=True, null=True)

    # Direccion
    tipo_via = models.CharField(max_length=255, blank=True, null=True, help_text='Calle/Avenida/Plaza...')
    nombre_via = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=255, blank=True, null=True)
    bloque = models.CharField(max_length=255, blank=True, null=True)
    escalera = models.CharField(max_length=255, blank=True, null=True)
    planta = models.CharField(max_length=255, blank=True, null=True)
    puerta = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)
    provincia = models.CharField(max_length=255, blank=True, null=True)
    municipio = models.CharField(max_length=255, blank=True, null=True)
    codigo_postal = models.CharField(max_length=255, blank=True, null=True)

    comentarios = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-nombre"]
        verbose_name = 'Tercero'
        verbose_name_plural = "Terceros"

    def __str__(self):
        if self.primer_apellido and self.segundo_apellido:
            return '{} {} {}'.format(self.primer_apellido, self.segundo_apellido, self.nombre)
        elif not self.primer_apellido and self.segundo_apellido:
            return '{} {}'.format(self.segundo_apellido, self.nombre)
        elif self.primer_apellido and not self.segundo_apellido:
            return '{} {}'.format(self.primer_apellido, self.nombre)
        else:
            return '{}'.format(self.nombre)