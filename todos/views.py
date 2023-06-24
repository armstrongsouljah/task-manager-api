from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import TodoItem, TodoList
from . import serializers as sz
from common.utils import CustomPagination
from authentication.models import UserProfile

import logging

log = logging.getLogger(__name__)

# Create your views here.
class TodoItemViewset(viewsets.ModelViewSet):
    """ Class to handle all requests for todo items """

    queryset = TodoItem.objects.all().select_related('created_by', 'created_by__user', 'todo_list')
    serializer_class = sz.TodoItemSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return sz.TodoItemSerializer
        return sz.TodoItemDisplaySerializer

    def get_queryset(self):
        return super().get_queryset()
    
    @action(detail=False, url_path='complete', methods=['PATCH'])
    def mark_todo_completed(self, request):
        payload = request.data
        params = request.query_params
        pk = params.get('pk')
        is_completed = payload.get('is_completed')
        request_user = request.user.userprofile
        item_msg = None

        item = get_object_or_404(TodoItem, pk=pk)
        serializer = sz.TodoItemSerializer(item, data=payload, partial=True)

        if item.created_by != request_user:
            return Response({
                'success': False,
                'msg': 'Can only update your item.'
            }, status=status.HTTP_403_FORBIDDEN)

        if  is_completed is None:
            return Response({
            'success': False,
            'msg': "is_completed must be true or false"
        }, status=status.HTTP_400_BAD_REQUEST)


        if not serializer.is_valid():
            return Response({
            'success': False,
            'msg': "Item could not be completed"
        }, status=status.HTTP_400_BAD_REQUEST)

        try:
            item.is_completed = bool(payload.get('is_completed'))
            if is_completed:
                item_msg = "Item marked completed"
            item_msg = "Item unmarked."
            item.save(update_fields=[
                'is_completed'
            ])
        except Exception as e:
            log.info(e)
            if not serializer.is_valid():
               return Response({
                    'success': False,
                    'msg': "Error marking item as completed"
                    }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'msg': item_msg
        })
    

    @action(detail=False, url_path="new-item", methods=["POST"])
    def create_new_item(self, request):
        payload = request.data
        list_id = payload.get("todo_list")

        request_user = self.request.user.userprofile
        payload['created_by'] = request_user.pk

        serializer = self.serializer_class(data=payload)


        if not serializer.is_valid():
            return Response({
            'success': False,
            'msg': serializer.errors,
            'data': {},
        }, status=status.HTTP_400_BAD_REQUEST)

        try:
            is_active = payload.get('is_active')
            todo_list = TodoList.objects.get(pk=list_id)
            
            if is_active:
                payload['is_active'] = bool(is_active)

            payload['created_by'] = request_user
            payload['todo_list'] = todo_list

            todo_item, _ = TodoItem.objects.get_or_create(**payload)
        except Exception as e:
            print(e)
            return  Response({
            'success': False,
            'msg': 'Error saving todo list',
            'data': {},
        }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'msg': 'Added new item to list',
            'data': sz.TodoListSerializer(todo_list).data,
        }, status=status.HTTP_201_CREATED)

class TodoListViewset(viewsets.ModelViewSet):
    """ Class to handle all requests for todo items """
    queryset = TodoList.objects.all()
    serializer_class = sz.TodoListSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return sz.TodoListSerializer
        return sz.TodoListDisplaySerializer

    def get_queryset(self):
        request_user = self.request.user.userprofile
        return self.queryset.filter(
            is_active=True, owner=request_user)
    
    @action(detail=False, url_path="new-list", methods=["POST"])
    def create_new_list(self, request):
        payload = request.data
        # owner_id = payload.get("owner")
        request_user = self.request.user.userprofile

        serializer = self.serializer_class(data=payload)


        if not serializer.is_valid():
            return Response({
            'success': False,
            'msg': serializer.errors,
            'data': {},
        }, status=status.HTTP_400_BAD_REQUEST)

        try:
            is_active = payload.get('is_active')
            
            if is_active:
                payload['is_active'] = bool(is_active)
            payload['owner'] = request_user
            todo_list, _ = TodoList.objects.get_or_create(**payload)
        except Exception as e:
            print(e)
            return  Response({
            'success': False,
            'msg': 'Error saving todo list',
            'data': {},
        }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'msg': 'Created new todo list',
            'data': sz.TodoListSerializer(todo_list).data,
        }, status=status.HTTP_201_CREATED)
    

    @action(methods=["PATCH"], url_path="update", detail=False)
    def update_list(self, request):
        payload = request.data
        params = request.query_params
        short_code = params.get("short_code")
        request_user = self.request.user.userprofile

        todo_list = get_object_or_404(TodoList, short_code=short_code)
        if todo_list.owner != request_user:
            return Response({
                'success': False,
                'msg': 'Can only update your lists.'
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = sz.TodoListSerializer(todo_list, data=payload, partial=True)

        if not serializer.is_valid():
            return Response({
            'success': False,
            'msg': 'Error updating the todo list'
        }, status=status.HTTP_400_BAD_REQUEST)

        try:
            title = payload.get('title')
            is_active = payload.get('is_active')
            is_completed = payload.get('is_completed')

            if is_completed:
                todo_list.is_completed = is_completed
                items = todo_list.todos.all()
                for item in items:
                    item.is_completed = is_completed
                TodoItem.objects.bulk_update(items, fields=['is_completed'])

            if is_active:
                todo_list.is_active = bool(is_active)
            if title:
                todo_list.title = title
            todo_list.save(update_fields=['title', 'is_active'])
        except Exception as e:
            print(e)
            return Response({
            'success': False,
            'msg': 'Could not complete editing the list',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'success': True,
            'msg': 'Todo list updated successfully.',
        }, status=status.HTTP_200_OK)
