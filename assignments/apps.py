from django.apps import AppConfig
import os
from django.conf import settings

class AssignmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assignments'
    path = os.path.join(settings.BASE_DIR, 'assignments')