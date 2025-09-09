from django.apps import AppConfig
import os
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    path = os.path.join(settings.BASE_DIR, 'users')
