from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from common.models import BaseModel
from django.conf import settings
from datetime import datetime as dt, timedelta
import jwt
from common import constants as cs

import logging

log = logging.getLogger(__name__)

# Create your models here.
class UserManager(BaseUserManager):
    """Manager for custom user model"""

    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        
        user  = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None):
        if not password:
            raise ValueError("Super user must have a password.")
        
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True 
        user.admin = True
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=250, unique=True)
    is_active=models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

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
    

    def token(self):
        """This method allows us to get users' token by calling 'user.token'"""
        return self.generate_jwt_token()
