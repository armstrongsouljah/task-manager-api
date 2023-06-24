import jwt
from django.conf import settings
from rest_framework import authentication as auth, exceptions as ex
from django.contrib.auth import get_user_model
from common import constants as cs

User = get_user_model()
# SECRET_KEY = getattr(settings, 'SECRET_KEY')

class JWTAuthentication(auth.BaseAuthentication):
    """Custom authentication backend"""

    def authenticate(self, request):
        auth_header = auth.get_authorization_header(request)
        prefix, token = None, None
        if auth_header:
            auth_header = auth.get_authorization_header(request).split()
            prefix = auth_header[0].decode('utf-8')
            token = auth_header[1].decode('utf-8')

        if auth_header and  len(auth_header) != 2:
            msg = "Invalid Token detected"
            raise ex.AuthenticationFailed(msg)

        if prefix and prefix != 'Bearer':
            msg = 'Use a Bearer Token'
            raise ex.AuthenticationFailed(msg)
        if request and token:
            return self.authenticate_credentials(request, token)
        pass
    

    def authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(
                token, cs.SECRET_KEY, algorithms='HS256')
        except (jwt.InvalidTokenError,jwt.ExpiredSignatureError,) :
            msg = 'Invalid token. Could not decode token'
            raise ex.AuthenticationFailed(msg)
        
        try:
            email = payload['user_data']
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            msg = "No user matching this token"
            raise ex.AuthenticationFailed(msg)
            
        # token_data = payload['user_data'].split()
        if not user.is_active:
            msg = "User has been deactivated"
            raise ex.AuthenticationFailed(msg)

        return (user, token)
    