from rest_framework import serializers

from .models import TodoItem, TodoList

# from authentication.serializers import UserProfileDisplaySerializer


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'

    def validate(self, data):
        todo_list_owner = data.get('todo_list').owner
        todo_list = data.get('todo_list')
        created_by = data.get('created_by')
        name = data.get('name')
        if todo_list_owner != created_by:
            raise serializers.ValidationError("Please select your own list")

        name_exists = todo_list.todos.filter(name__iexact=name).exists()
        if name_exists:
            raise serializers.ValidationError("Item already added to list.")
        return data


class TodoListSerializer(serializers.Serializer):
    class Meta:
        model = TodoList
        fields = '__all__'

    def validate(self, data):
        title = data.get('title')
        print('title....', title)

        name_exists = TodoList.objects.filter(title__iexact=title).exists()
        if name_exists:
            raise serializers.ValidationError("A list with the same title exists.")
        return data


class TodoItemDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = [
            'pk',
            'name',
            'is_active',
            'is_completed',
        ]


class TodoListDisplaySerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    title = serializers.CharField()
    owner = serializers.CharField()
    is_completed = serializers.BooleanField()
    is_active = serializers.BooleanField()
    short_code = serializers.CharField()
    todos = TodoItemDisplaySerializer(many=True, read_only=True)

    class Meta:
        fields = ['pk', 'title', 'todos', 'owner', 'is_completed', 'is_active', 'short_code']
