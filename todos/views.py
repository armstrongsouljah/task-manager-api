from django.shortcuts import render
from rest_framework import viewsets
from .models import TodoItem, TodoList
from . import serializers as sz
from common.utils import CustomPagination

# Create your views here.
class TodoItemViewset(viewsets.ModelViewSet):
    """ Class to handle all requests for todo items """

    queryset = TodoItem.objects.all().select_related('created_by', 'created_by__user', 'todo_list')
    serializer_class = sz.TodoItemSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return sz.TodoItemSerializer
        return sz.TodoItemDisplaySerializer

    def get_queryset(self):
        return super().get_queryset()
    

class TodoListViewset(viewsets.ModelViewSet):
    """ Class to handle all requests for todo items """
    
    queryset = TodoList.objects.all()
    serializer_class = sz.TodoListSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return sz.TodoListSerializer
        return sz.TodoListDisplaySerializer

    def get_queryset(self):
        return super().get_queryset()
