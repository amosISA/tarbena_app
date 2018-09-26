# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from .models import Subvencion
from .tasks import task_alert_changed_estado

@receiver(post_save, sender=Subvencion)
def check_changed_estado(sender, instance, **kwargs):
    """"
    If you create new user, a new profile will be created for that user
    Create the profile object, only if it is newly created

    """

    # https://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed
    # gives the ids of estados (1, 2)
    # this means that is was on estado with id 1 and we changed it to estado with id 2
    estado_diff = instance.get_field_diff('estado')
    if estado_diff:
        a, b = estado_diff

        if b == 1 or b == 3:
            # task_alert_changed_estado.delay(instance, instance.nombre, b, 'https://google.es',
            #                                 'amosisa700@gmail.com', ['amosisa700@gmail.com', 'jctarbena@gmail.com'])

            # This executes one time after two months
            task_alert_changed_estado.apply_async(args=[instance, instance.nombre, b,
                                                         'https://google.es',
                                                         'amosisa700@gmail.com',
                                                         ['amosisa700@gmail.com', 'jctarbena@gmail.com']
                                                         ], countdown=5184000)
