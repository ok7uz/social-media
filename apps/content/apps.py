from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = 'config.utils.CustomAutoField'
    name = 'apps.content'
