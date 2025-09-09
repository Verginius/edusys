from django.apps import AppConfig
import os
from django.conf import settings


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
    path = os.path.join(settings.BASE_DIR, 'courses')
