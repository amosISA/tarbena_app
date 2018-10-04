from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group

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

class FavouriteTypes(TimeStampedModel):
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ["name"]
        verbose_name = 'Tipos de favoritos'
        verbose_name_plural = "Tipos de favoritos"

    def __str__(self):
        return self.name

class Favourite(TimeStampedModel):
    name = models.CharField(max_length=250)
    link = models.TextField(blank=True)
    user = models.ManyToManyField(User, blank=True, related_name='favourite_users')
    group = models.ForeignKey(Group, blank=True, related_name='favourite_group')
    type = models.ForeignKey(FavouriteTypes, related_name='favourite_types')

    class Meta:
        ordering = ["name"]
        verbose_name = 'Favoritos'
        verbose_name_plural = "Favoritos"

    def __str__(self):
        return self.name