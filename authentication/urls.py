from rest_framework.routers import DefaultRouter
from . import views as auth_views

router = DefaultRouter()

router.register('register', auth_views.UserRegistrationViewset, basename='register')


app_name = 'authentication'

urlpatterns = []

urlpatterns += router.urls