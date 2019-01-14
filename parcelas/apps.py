from django.apps import AppConfig


class ParcelasConfig(AppConfig):
    name = 'parcelas'

    def ready(self):
        # Setup the signals for Parcelas
        from . import signals