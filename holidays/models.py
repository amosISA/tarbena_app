from django.db import models

# Create your models here.
class Holiday(models.Model):
    date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.date)

    class Meta:
        ordering = ['date',]