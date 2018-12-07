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
    email = models.CharField(max_length=250, default="", blank=True, null=True)
    telefono = models.CharField(max_length=250, default="", blank=True, null=True)
    direccion = models.CharField(max_length=250, default="", blank=True, null=True)
    provincia = models.CharField(max_length=250, default="", blank=True, null=True)
    poblacion = models.CharField(max_length=250, default="", blank=True, null=True)
    color = models.CharField(max_length=250, default="", blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["name"]

class Organos(TimeStampedModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ["name"]
        verbose_name = 'Organos'
        verbose_name_plural = "Organos"

class AplicacionPresupuestaria(TimeStampedModel):
    aplicacion_presupuestaria = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.aplicacion_presupuestaria)

    class Meta:
        ordering = ["aplicacion_presupuestaria"]

class Cpv(TimeStampedModel):
    cpv = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.cpv)

    class Meta:
        ordering = ["cpv"]

class Contract(TimeStampedModel):
    type = models.ForeignKey(TypeContract, related_name='type_contract', blank=True, null=True)
    contractor = models.ForeignKey(Contractor, related_name='contract_contractor', blank=True, null=True)
    base = models.CharField(max_length=250, blank=True, null=True)
    iva = models.CharField(max_length=250, blank=True, null=True)
    total = models.CharField(max_length=250, blank=True, null=True)
    date_contract = models.DateField(blank=True, null=True)
    cpv = models.ManyToManyField(Cpv, related_name='cpvs', blank=True)
    duracion = models.CharField(max_length=250, blank=True, null=True)
    objeto = models.TextField(blank=True, help_text='Necesidad a satisfacer / Objeto del contrato')
    aplic_presupuestaria = models.ForeignKey(AplicacionPresupuestaria, related_name='contract_aplicacion_presupuestaria', default='', blank=True, null=True)
    description = models.TextField(blank=True)

    # Aplicacion presupuestaria
    ejercicio = models.CharField(max_length=250, blank=True, null=True)
    importe_recursos = models.CharField(max_length=250, blank=True, null=True,
                                        help_text='Importe de los recursos del presupuesto')
    valor_estimado = models.CharField(max_length=250, blank=True, null=True, help_text='Valor estimado del contrato')
    porcentaje = models.CharField(max_length=250, blank=True, null=True, help_text='% sobre los recursos')
    organo = models.ForeignKey(Organos, related_name='aplic_presup_organo', blank=True, null=True)

    decl_responsable = models.BooleanField(default=False, help_text='Declaración responsable de no incurrir en prohibición de contratar')
    certificado_hacienda = models.BooleanField(default=False, help_text='Certificado Hacienda de estar al corriente de sus obligaciones')

    class Meta:
        ordering = ["type"]
        verbose_name = 'Contratos'
        verbose_name_plural = "Contratos"

    def __str__(self):
        return '{}, {}'.format(self.type, self.contractor)