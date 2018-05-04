# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# Create your models here.
def upload_location(instance, filename):
    username = instance.user.username
    return "profiles/avatar/%s/%s_%s" % (username, username, filename)

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

class Profile(TimeStampedModel):
    user = models.OneToOneField(User, primary_key=True)
    avatar = models.ImageField(upload_to=upload_location,
                               null=True,
                               blank=True,
                               height_field="height_field",
                               width_field="width_field")
    height_field = models.IntegerField(default=0, blank=True, null=True)
    width_field = models.IntegerField(default=0, blank=True, null=True)
    telefono = models.CharField(max_length=250, blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.user.username



