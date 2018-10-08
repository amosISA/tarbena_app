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

class TypeContract(TimeStampedModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["name"]

class Contractor(TimeStampedModel):
    name = models.CharField(max_length=250)
    dni = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["name"]

class Contract(TimeStampedModel):
    type = models.ForeignKey(TypeContract, related_name='type_contract', blank=True, null=True)
    contractor = models.ForeignKey(Contractor, related_name='contract_contractor', blank=True, null=True)
    base = models.CharField(max_length=250, blank=True, null=True)
    iva = models.CharField(max_length=250, blank=True, null=True)
    total = models.CharField(max_length=250, blank=True, null=True)
    date_contract = models.DateField(blank=True, null=True)
    cpv = models.CharField(max_length=250, blank=True, null=True)
    duracion = models.CharField(max_length=250, blank=True, null=True)
    objeto = models.TextField(blank=True)
    aplicacion_presupuestaria = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["type"]
        verbose_name = 'Contratos'
        verbose_name_plural = "Contratos"

    def __str__(self):
        return '{}, {}'.format(self.type, self.contractor)