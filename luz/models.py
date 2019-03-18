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

class Contador(TimeStampedModel):
    nombre = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = 'Contador'
        verbose_name_plural = "Contadores"

    def __str__(self):
        return '{}'.format(self.nombre)

class Factura(TimeStampedModel):
    desde = models.DateField(blank=True, null=True)
    hasta = models.DateField(blank=True, null=True)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    lectura_anterior = models.CharField(max_length=250, blank=True, null=True)
    lectura_posterior = models.CharField(max_length=250, blank=True, null=True)
    consumo = models.CharField(max_length=250, blank=True, null=True)
    contador = models.ForeignKey(Contador, blank=True, null=True, related_name='contadores')

    class Meta:
        ordering = ["desde"]
        verbose_name = 'Factura'
        verbose_name_plural = "Facturas"

    def __str__(self):
        return '{}'.format(self.contador.nombre)
