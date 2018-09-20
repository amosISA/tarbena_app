from django.apps import AppConfig


class SubvencionesConfig(AppConfig):
    name = 'subvenciones'

    def ready(self):
        # Setup the signals for Subvenciones
        from . import signals