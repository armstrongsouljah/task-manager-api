from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import permissions as p
from . import serializers as sz
import logging

log = logging.getLogger(__name__)


User = get_user_model()

# Create your views here.
class UserRegistrationViewset(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (p.AllowAny,)
    serializer_class  = sz.RegistrationSerializer
    
    def create(self, request):
        payload = request.data
       
        serializer = self.serializer_class(data=payload)
        if not serializer.is_valid():
            return Response({
            'success': False,
            'data': None,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            email = payload.get('email')
            password = payload.get('password')
            user, _ = User.objects.get_or_create(email=email, password=password)
         
        except Exception as e:
            return Response({
            'success': False,
            'data': None,
            'msg': f"Error creating a new user. {e}"
        }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'data': sz.RegistrationSerializer(user).data
        }, status=status.HTTP_201_CREATED)