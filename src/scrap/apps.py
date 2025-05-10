import os
from django.apps import AppConfig


class ScrapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrap'
    verbose_name = 'Агрегатор вакансий'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            return  # предотвращаем двойной запуск при autoreload

        from .scheduler import start
        start()
