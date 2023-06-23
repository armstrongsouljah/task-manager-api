from django.db import models

# Create your models here.
class BaseModel(models.Model):
    """To be utilized by other models with shared fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)