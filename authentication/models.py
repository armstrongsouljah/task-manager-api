from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from datetime import datetime as dt, timedelta
import jwt
from common import constants as cs
from django.db.models.signals import post_save

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
    is_active=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
