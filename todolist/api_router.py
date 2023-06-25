from rest_framework.routers import DefaultRouter, SimpleRouter

from common import constants as cst

if cst.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# todos
