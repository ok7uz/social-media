from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'config.utils.CustomAutoField'
    name = 'apps.chat'
