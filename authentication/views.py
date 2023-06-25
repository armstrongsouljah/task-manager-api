from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import permissions as p
from . import serializers as sz
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from common.utils import send_activation_email, email_verification_token, generate_verification_url
from datetime import datetime
from .models import PasswordResetManager
import logging

log = logging.getLogger(__name__)


User = get_user_model()

# Create your views here.
class UserRegistrationViewset(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (p.AllowAny,)
    serializer_class  = sz.RegistrationSerializer

    @action(detail=False, url_path="new", methods=["POST"])
    def register_user(self, request):
        payload = request.data
        serializer = self.serializer_class(data=payload)
        if not serializer.is_valid():

            return Response({
            'success': True,
            'msg': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
           email = payload.get('email')
           password = payload.get('password')
           user = User.objects.create_user(email=email, password=password)
           
           email_details = generate_verification_url(user, request)
           url = email_details.get('url')
           username = email_details.get('username')
           email = email_details.get('email')
           email_sent = send_activation_email.delay(url=url, username=username, email=email)

           if not email_sent:
               log.info("Email sending failed.....")

        except Exception as e:

            return Response({
            'success': True,
            'msg': f'Could not register new user, {e}'
        }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'msg': 'Successfully registered a new user, please check your email to activate account.',
            'token': user.token
        }, status=status.HTTP_201_CREATED)
    

class EmailVerificationViewset(GenericAPIView):
    def get(self, request, uuid, token):
        try:
            user_id = force_bytes(urlsafe_base64_decode(uuid)).decode('utf-8')
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({
            'msg': "Error verifying email"
        }, status=status.HTTP_400_BAD_REQUEST)
        
        if user is not None and email_verification_token.check_token(user, token):
            user.email_verified = True
            user.email_verification_date = datetime.utcnow()
            user.is_active = True
            user.save()
        return Response({
            'msg': "Email successfully verified"
        }, status=status.HTTP_200_OK)
    
class LoginViewset(ViewSet):
    permission_classes = (p.AllowAny,)
    serializer_class = sz.LoginSerializer

    @action(methods=["POST"],url_path="user", detail=False)
    def perform_login(self,request):
        payload = request.data
        serialiser = self.serializer_class(data=payload)
        if not serialiser.is_valid():
            return Response({
            "success": False,
            "error": serialiser.errors,
            "token":""
        })
       
        token = serialiser.data.get('token')
        if not token:
            return Response({
            "msg": "Invalid username or password",
            "token": None
        }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "msg": "Successfully logged in",
            "token": token
        }, status=status.HTTP_200_OK)
    

class AccountDeactivationViewset(ViewSet):
    permission_classes = (p.IsAuthenticated,)
    @action(methods=["POST"], url_path="deactivate", detail=False)
    def deactivate_account(self, request):
        user = request.user
        user.is_active = False
        user.email_verified = False
        user.save(update_fields=['is_active', 'email_verified'])
        return Response({
            'success': True,
            'msg': 'Account deactivated'
        }, status=status.HTTP_202_ACCEPTED)
    

class ResetPasswordAPIView(GenericAPIView):
    permission_classes = (p.AllowAny,)
    serializer_class = sz.PasswordResetSerializer   

    def put(self, request,token):
        payload = request.data
        reset_manager = PasswordResetManager(request)
        user = reset_manager.get_user_from_token(token)

        if not user:
            return Response(
            {  
                "success": False,
                "msg":"Could not reset password",
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        password = data.get('password')
        user.set_password(password)
        user.save()
        return Response(
            {  
                "success": True,
                "msg":"Your password has been updated",
            }, status=status.HTTP_202_ACCEPTED)
    

class RequestPasswordResetAPIView(GenericAPIView):
    permission_classes = (p.AllowAny,)
    serializer_class = sz.PasswordResetRequestSerializer

    def post(self, request):
        """
        When a user posts an email here.
        It's validated and a 'password reset email' is sent
        to their registered email
        """
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data.get('email',None)
        reset_manager = PasswordResetManager(request)
        reset_manager.request_password_reset(user_email)
        return Response({'msg':'Email sent. Please check your inbox for a password reset email.'}, status = status.HTTP_200_OK)

