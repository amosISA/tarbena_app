from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete

from . import models
from .utils import delete_file

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, created, **kwargs):
    if not created:
        return
    # Create the profile object, only if it is newly created
    profile = models.Profile(user=instance)
    profile.save()

# Delete image after uploading a new one
@receiver(post_init, sender=models.Profile)
def backup_image_path(sender, instance, **kwargs):
    instance._current_imagen_file = instance.avatar

@receiver(post_save, sender=models.Profile)
def delete_img_post_update(sender, instance, **kwargs):
    if hasattr(instance, '_current_imagen_file'):
        if instance.avatar:
            if instance._current_imagen_file != instance.avatar.path:
                instance._current_imagen_file.delete(save=False)
        else:
            if instance._current_imagen_file:
                instance._current_imagen_file.delete()

#Delete image after the profile user is deleted
@receiver(post_delete, sender=models.Profile)
def delete_img_post_delete(sender, instance, *args, **kwargs):
    if instance.avatar:
        delete_file(instance.avatar.path)