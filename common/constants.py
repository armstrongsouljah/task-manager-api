from django.conf import settings

SECRET_KEY = getattr(settings, 'SECRET_KEY')
DEBUG = getattr(settings, 'DEBUG')
DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')
