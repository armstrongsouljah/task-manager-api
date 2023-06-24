from rest_framework import serializers as sz
from .models import User
import re
from django.contrib.auth import authenticate

class RegistrationSerializer(sz.ModelSerializer):
    class Meta:
        model = User
        fields = ['email',  'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        email = value
        # Regular expression pattern for email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
        # Check if the email matches the pattern
        if not re.match(pattern, email):
            raise sz.ValidationError("Invalid email address")
        else:
            return email
        
    def validate_password(self, password):
        # Check length
        if len(password) < 5:
            raise sz.ValidationError("Password must be 5 characters or longer")
    
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise sz.ValidationError("Password must contain at least 1 uppercase letter.")
    
        # Check for at least one digit
        if not re.search(r'\d', password):
            raise sz.ValidationError("Password must contain at least 1 digit")
        return password
    
class LoginSerializer(sz.Serializer):
    email = sz.CharField(max_length=255, required=True)
    password = sz.CharField(max_length=128, write_only=True)
    token = sz.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        print(email, password)

        # email validation
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
        # Check if the email matches the pattern
        if not re.match(pattern, email):
            raise sz.ValidationError("Invalid email address")
        
        if not password:
            raise sz.ValidationError("Password required.")
        
        user = authenticate(username=email, password=password)
        print('user.......',user)

        if not user:
            raise sz.ValidationError("Invalid username or password.")
    
        return {
            'email': user.email,
            'token': user.token
        }
    

class UserProfileDisplaySerializer(sz.Serializer):
    email = sz.CharField(source='user.email')
    fields = [
        'first_name',
        'last_name',
        'email'
    ]