from rest_framework.routers import DefaultRouter
from . import views as auth_views
from django.urls import path

router = DefaultRouter()

router.register('register', auth_views.UserRegistrationViewset, basename='register')
# router.register('verify', auth_views.EmailVerificationViewset, basename='verify')


app_name = 'authentication'

urlpatterns = [
    path('verify/<uuid>/<token>', auth_views.EmailVerificationViewset.as_view(), name='email-verification'),
]

urlpatterns += router.urls