from django.db import models
from django.db.models.signals import post_save

from authentication.models import UserProfile

from .utils import unique_code_generator


# Create your models here.
class TodoList(models.Model):
    is_active = models.BooleanField(default=True)
    is_recurring = models.BooleanField(default=False)
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    short_code = models.CharField(max_length=35, blank=True, null=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='my_todo_list')

    def __str__(self):
        return f"{self.title}"


class TodoItem(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='todos')
    name = models.CharField(max_length=120)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='author')
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.todo_list.title}, {self.name}'


def todo_list_post_save_receiver(instance, sender, created, **kwargs):
    if created:
        instance.short_code = unique_code_generator(size=8)
        instance.save()


post_save.connect(todo_list_post_save_receiver, sender=TodoList)
