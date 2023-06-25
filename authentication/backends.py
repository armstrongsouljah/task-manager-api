import jwt
from django.contrib.auth import get_user_model
from rest_framework import authentication as auth
from rest_framework import exceptions as ex

from common import constants as cs

User = get_user_model()


class JWTAuthentication(auth.BaseAuthentication):
    """Custom authentication backend"""

    def authenticate(self, request):
        auth_header = auth.get_authorization_header(request)
        prefix, token = None, None

        if auth_header:
            auth_header = auth.get_authorization_header(request).split()
            prefix = auth_header[0].decode('utf-8')
            token = auth_header[1].decode('utf-8')

        if auth_header and len(auth_header) != 2:
            msg = "Invalid Token detected"
            raise ex.AuthenticationFailed(msg)

        if prefix and prefix != 'Bearer':
            msg = 'Use a Bearer Token'
            raise ex.AuthenticationFailed(msg)
        if request and token:
            return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, cs.SECRET_KEY, algorithms='HS256')
        except (
            jwt.InvalidTokenError,
            jwt.ExpiredSignatureError,
        ):
            msg = 'Invalid token. Could not decode token'
            raise ex.AuthenticationFailed(msg)

        try:
            email = payload['user_data']
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            msg = "No user matching this token"
            raise ex.AuthenticationFailed(msg)

        # ensure only valid emails access the platform
        if not user.is_active and not user.email_verified:
            msg = "Account not activate or account has been deactivated"
            raise ex.AuthenticationFailed(msg)

        return (user, token)
