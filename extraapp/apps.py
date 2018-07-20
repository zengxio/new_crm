from django.apps import AppConfig


class ExtraappConfig(AppConfig):
    name = 'extraapp'

    def ready(self):
        super(ExtraappConfig,self).ready()
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('exapp')