from rest_framework.routers import DefaultRouter
from . import views as td
from django.urls import path

router = DefaultRouter()

router.register('items/all', td.TodoItemViewset, basename='todos')
router.register('lists', td.TodoListViewset, basename='todolist')



app_name = 'authentication'

urlpatterns = [
]

urlpatterns += router.urls