from django.conf import settings


SECRET_KEY = getattr(settings, 'SECRET_KEY')
DEBUG = getattr(settings, 'DEBUG')
