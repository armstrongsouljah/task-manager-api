from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from datetime import datetime as dt, timedelta
import jwt
from common import constants as cs
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
import datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from rest_framework import serializers
from .utils import send_gen_email
from rest_framework import exceptions as ex

import logging

log = logging.getLogger(__name__)

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Manager for custom user model"""

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user  = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **kwargs):
        if not password:
            raise ValueError("Super user must have a password.")
        
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True 
        user.admin = True
        user.save()
        return user



class User(AbstractBaseUser, PermissionsMixin):
    username=None
    email = models.EmailField(max_length=250, unique=True)
    is_active=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'
    
    @property
    def get_full_name(self):
        return self.email.split('@')[0].capitalize()
    
    @property
    def get_short_name(self):
        return self.email
    

    def generate_jwt_token(self):
        """This generates a JSON Web Token that stores"""
        token_string = f'{self.email}'
        token = jwt.encode(
            {
                'user_data': token_string,
                'exp': dt.now() + timedelta(hours=5)
            }, cs.SECRET_KEY, algorithm='HS256'
        )
        return token
    
    @property
    def token(self):
        """This method allows us to get users' token by calling 'user.token'"""
        return self.generate_jwt_token()
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}"
    

def user_post_save_receiver(instance, created, *args, **kwargs):
    """
    Handle creating the profile when a user finishes
    the signup process
    """
    if created:
        UserProfile.objects.get_or_create(
            user=instance,
        )
post_save.connect(user_post_save_receiver, sender=User)


class PasswordResetManager(object):
    """
    This handles password reset requests
    password reset link verifications and
    updating the user model with the new password
    """

    def __init__(self,request):
        """prepare up email params"""
        self.sender_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        self.token_generator = PasswordResetTokenGenerator()
        self.subject = "Reset your Password"
        self.account_recovery_endpoint = request.build_absolute_uri('/auth/users/password-reset/')

    def request_password_reset(self,email):
        """Handles request to reset email"""
        user = self.find_user_by_email(email)

        if user is None:
            raise serializers.ValidationError("User with that email does not exist.")

        self.receiver_email = user.email

        #generate user token to be used in password reset link
        token = jwt.encode({'email': user.email,
                             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                             },
                            settings.SECRET_KEY
                            ,algorithm='HS256')

        #render password reset email from template
        context = {
            'username' : user.email.split('@')[0],
            'action_url' : self.account_recovery_endpoint+token,
            'app_name': "Todos Manager"
        }
        rendered_string =  render_to_string('password_reset_email.html', context)


   #send password reset email to user
        return (
            send_gen_email.delay(
            subject=self.subject,
            email_body=rendered_string,
            sender_mail=self.sender_email,
            receipients=[user.email,]),token)

    def get_user_from_token(self,token):
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256',])
            return self.find_user_by_email(payload['email'])
        except (jwt.ExpiredSignatureError,):
            msg="Token expired"
            raise ex.AuthenticationFailed(msg)

    def find_user_by_email(self,email):
        email = CustomUserManager.normalize_email(email)
        try:
            user =  User.objects.get(email=email)
            return user
        except:
            return None

