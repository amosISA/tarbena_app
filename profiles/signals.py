# -*- coding: utf-8 -*-
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete, pre_save
from django.contrib.auth.models import Group
from datetime import datetime

from . import models
from .utils import delete_file

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, created, **kwargs):
    """"
    If you create new user, a new profile will be created for that user
    Create the profile object, only if it is newly created

    Also add him to ciudadanos Group

    """
    try:
        if Group.objects.get(name='ciudadanos'):
            group = Group.objects.get(name='ciudadanos')
            instance.groups.add(group)
    except Group.DoesNotExist:
        pass

    if not created:
        return
    profile = models.Profile(user=instance)
    profile.save()

@receiver(pre_save, sender=models.Profile)
def save_created_field(sender, instance, **kwargs):
    """" Save created field on profile """

    instance.created = datetime.now()

# @receiver(post_init, sender=models.Profile)
# def backup_image_path(sender, instance, **kwargs):
#     """" Delete image after uploading a new one """
#
#     instance._current_imagen_file = instance.avatar
#
# @receiver(post_save, sender=models.Profile)
# def delete_img_post_update(sender, instance, **kwargs):
#     """" Delete image after uploading a new one """
#
#     if hasattr(instance, '_current_imagen_file'):
#         if instance.avatar:
#             if instance._current_imagen_file != instance.avatar.path:
#                 instance._current_imagen_file.delete(save=False)
#         else:
#             if instance._current_imagen_file:
#                 instance._current_imagen_file.delete()
#
# @receiver(post_delete, sender=models.Profile)
# def delete_img_post_delete(sender, instance, *args, **kwargs):
#     """ Delete image after the profile user is deleted """
#
#     if instance.avatar:
#         delete_file(instance.avatar.path)