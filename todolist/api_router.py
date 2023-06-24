from rest_framework.routers import DefaultRouter, SimpleRouter
from common import constants as cst

from authentication import views as auth

if cst.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# todos
