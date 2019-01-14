# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from . import models

@receiver(post_save, sender=models.Parcela)
def create_kml_field(sender, update_fields, instance, created, **kwargs):
    """"
    Create the kml field into the parcela object after we create it

    """
    pass