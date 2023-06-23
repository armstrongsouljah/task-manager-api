from rest_framework import serializers as sz
from .models import User
import re

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
        
    