from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views as auth_views

router = DefaultRouter()

router.register('register', auth_views.UserRegistrationViewset, basename='register')
router.register("login", auth_views.LoginViewset, basename="login")
router.register("account", auth_views.AccountDeactivationViewset, basename="account-deactivation")


app_name = 'authentication'

urlpatterns = [
    path(
        'verify/<uuid>/<token>',
        auth_views.EmailVerificationViewset.as_view(),
        name='email-verification',
    ),
    path(
        'request-reset-link/',
        auth_views.RequestPasswordResetAPIView.as_view(),
        name='password-reset-request',
    ),
    path(
        'password-reset/<token>/', auth_views.ResetPasswordAPIView.as_view(), name='password-reset'
    ),
]

urlpatterns += router.urls
