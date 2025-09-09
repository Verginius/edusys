from django.apps import AppConfig
import os
from django.conf import settings


class QueryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'query'
    path = os.path.join(settings.BASE_DIR, 'query')
