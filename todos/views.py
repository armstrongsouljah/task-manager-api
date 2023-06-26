import logging

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.utils import CustomPagination

from . import serializers as sz
from .models import TodoItem, TodoList

log = logging.getLogger(__name__)

# Create your views here.


class TodoItemViewset(viewsets.ModelViewSet):
    """Class to handle all requests for todo items"""

    queryset = TodoItem.objects.all().select_related('created_by', 'created_by__user', 'todo_list')
    serializer_class = sz.TodoItemSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return sz.TodoItemSerializer
        return sz.TodoItemDisplaySerializer

    def get_queryset(self):
        request_user = self.request.user.userprofile
        search = self.request.query_params.get('search')
        sort = self.request.query_params.get('sort')
        sort_key = self.request.query_params.get('sort_key')

        queryset = self.queryset.filter(created_by=request_user).select_related(
            'created_by', 'created_by__user', 'todo_list'
        )
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(todo_list__title__icontains=search)
            )

        if (sort and sort.lower() == 'desc') and sort_key:
            queryset = queryset.order_by(f'-{sort_key}')

        if (sort and sort.lower() == 'asc') and sort_key:
            queryset = queryset.order_by(f'{sort_key}')

        return queryset

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
            return Response(
                {'success': False, 'msg': 'Can only update your item.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if is_completed is None:
            return Response(
                {'success': False, 'msg': "is_completed must be true or false"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not serializer.is_valid():
            return Response(
                {'success': False, 'msg': "Item could not be completed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            item.is_completed = bool(payload.get('is_completed'))
            if is_completed:
                item_msg = "Item marked completed"
            item_msg = "Item unmarked."
            item.save(update_fields=['is_completed'])
        except Exception as e:
            log.info(e)
            if not serializer.is_valid():
                return Response(
                    {'success': False, 'msg': "Error marking item as completed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response({'success': True, 'msg': item_msg})

    @action(detail=False, url_path='update', methods=['PATCH'])
    def update_todo_item(self, request):
        payload = request.data
        params = request.query_params
        pk = params.get('pk')
        request_user = request.user.userprofile

        item = get_object_or_404(TodoItem, pk=pk)
        serializer = sz.TodoItemSerializer(item, data=payload, partial=True)

        if item.created_by != request_user:
            return Response(
                {'success': False, 'msg': 'Can only update your item.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            name = payload.get('name')
            item.name = name
            item.save(
                update_fields=[
                    'name',
                ]
            )
        except Exception as e:
            log.info(e)
            if not serializer.is_valid():
                return Response(
                    {'success': False, 'msg': "Error updating todo item"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {
                'success': True,
                'msg': "Todo item updated.",
                'data': sz.TodoItemDisplaySerializer(item).data,
            }
        )

    @action(detail=False, url_path="new-item", methods=["POST"])
    def create_new_item(self, request):
        payload = request.data
        list_id = payload.get("todo_list")

        request_user = self.request.user.userprofile
        payload['created_by'] = request_user.pk

        serializer = self.serializer_class(data=payload)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'msg': serializer.errors,
                    'data': {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
            return Response(
                {
                    'success': False,
                    'msg': 'Error saving todo item',
                    'data': {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'success': True,
                'msg': 'Added new item to list',
                'data': sz.TodoItemSerializer(todo_item).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, url_path="delete-item", methods=["DELETE"])
    def delete_todo_item(self, request):
        request_user = request.user.userprofile
        item_id = request.query_params.get("pk")
        list_id = request.query_params.get("todo_list")

        todo_item = get_object_or_404(
            TodoItem, pk=item_id, created_by=request_user, todo_list__pk=list_id
        )
        try:
            TodoItem.objects.filter(pk=todo_item.pk).delete()
        except Exception as e:
            return Response(
                {'success': False, 'msg': f'Error deleting todo item, {e}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'success': True, 'msg': 'Todo item deleted'}, status=status.HTTP_204_NO_CONTENT
        )


class TodoListViewset(viewsets.ModelViewSet):
    """Class to handle all requests for todo lists"""

    queryset = TodoList.objects.all()
    serializer_class = sz.TodoListSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return sz.TodoListSerializer
        return sz.TodoListDisplaySerializer

    def get_queryset(self):
        request_user = self.request.user.userprofile
        search = self.request.query_params.get('search')
        sort = self.request.query_params.get('sort')
        sort_key = self.request.query_params.get('sort_key')
        queryset = self.queryset.filter(is_active=True, owner=request_user)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(todos__name__icontains=search)
            )

        if (sort and sort.lower() == 'desc') and sort_key:
            queryset = queryset.order_by(f'-{sort_key}')

        if (sort and sort.lower() == 'asc') and sort_key:
            queryset = queryset.order_by(f'{sort_key}')

        return queryset

    @action(detail=False, url_path="new-list", methods=["POST"])
    def create_new_list(self, request):
        payload = request.data
        request_user = self.request.user.userprofile

        serializer = self.serializer_class(data=payload)

        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'msg': serializer.errors,
                    'data': {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            is_active = payload.get('is_active')

            if is_active:
                payload['is_active'] = bool(is_active)
            payload['owner'] = request_user
            todo_list, _ = TodoList.objects.get_or_create(**payload)
            todo_list = TodoList.objects.latest('created_at')

        except Exception as e:
            print(e)
            return Response(
                {
                    'success': False,
                    'msg': 'Error saving todo list',
                    'data': {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'success': True,
                'msg': 'Created new todo list',
                'data': sz.TodoListDisplaySerializer(instance=todo_list).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(methods=["PATCH"], url_path="update", detail=False)
    def update_list(self, request):
        payload = request.data
        params = request.query_params
        short_code = params.get("short_code")
        request_user = self.request.user.userprofile

        todo_list = get_object_or_404(TodoList, short_code=short_code)
        if todo_list.owner != request_user:
            return Response(
                {'success': False, 'msg': 'Can only update your lists.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = sz.TodoListSerializer(todo_list, data=payload, partial=True)

        if not serializer.is_valid():
            return Response(
                {'success': False, 'msg': 'Error updating the todo list'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            title = payload.get('title')
            is_active = payload.get('is_active')
            is_completed = payload.get('is_completed')

            if is_completed:
                is_completed = bool(is_completed)
                todo_list.is_completed = bool(is_completed)
                items = todo_list.todos.all()
                for item in items:
                    item.is_completed = is_completed
                TodoItem.objects.bulk_update(items, fields=['is_completed'])
                todo_list.save(update_fields=['is_completed'])

            if is_active:
                todo_list.is_active = bool(is_active)
            if title:
                todo_list.title = title
            todo_list.save(update_fields=['title', 'is_active'])
        except Exception as e:
            print(e)
            return Response(
                {
                    'success': False,
                    'msg': 'Could not complete editing the list',
                    'error': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'success': True,
                'msg': 'Todo list updated successfully.',
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, url_path="delete-list", methods=["DELETE"])
    def delete_todo_list(self, request):
        request_user = request.user.userprofile
        list_id = request.query_params.get("pk")

        todo_list = get_object_or_404(TodoList, pk=list_id, owner=request_user)
        try:
            TodoList.objects.filter(pk=todo_list.pk).delete()
        except Exception as e:
            return Response(
                {'success': False, 'msg': f'Error deleting todo list, {e}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'success': True, 'msg': 'Todo list deleted'}, status=status.HTTP_204_NO_CONTENT
        )
