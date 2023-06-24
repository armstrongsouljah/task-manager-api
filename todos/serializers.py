from rest_framework import serializers
from .models import TodoList, TodoItem
from authentication.serializers import UserProfileDisplaySerializer

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TodoItem
        fields = '__all__'


class TodoListSerializer(serializers.Serializer):
    class Meta:
        model = TodoList
        fields = '__all__'


class TodoItemDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = [
            'name', 'is_active','is_completed',
            ]
    
class TodoListDisplaySerializer(serializers.Serializer):
    title = serializers.CharField()
    owner = serializers.CharField()
    is_completed = serializers.BooleanField()
    is_active = serializers.BooleanField()
    todos = TodoItemDisplaySerializer(many=True, read_only=True)
    
    
    class Meta:
        fields = [
             
             'title', 'todos', 'owner', 'is_completed', 'is_active'
             ]                                                                                                                                                                                                                                                                                                                                                                                                           