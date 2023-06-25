from django.test import Client, TestCase
from django.utils import timezone as dt

from .models import User, UserProfile

# Create your tests here.


class RegistrationTest(TestCase):
    """Test user registration implementation"""

    def setUp(self):
        self.client = Client()

    def test_sucessful_user_signup(self):
        signup_url = '/auth/users/register/'
        payload = {'email': 'testuser@gmail.com', 'password': 'Password2'}
        response = self.client.post(signup_url, payload)
        self.assertEqual(201, response.status_code)

    def test_signup_with_invalid_email(self):
        signup_url = '/auth/users/register/'
        payload = {'email': 'testusergmail.com', 'password': 'Password2'}
        response = self.client.post(signup_url, payload)
        self.assertEqual(400, response.status_code)

    def test_signup_without_password_fails(self):
        signup_url = '/auth/users/register/'
        payload = {'email': 'testuser@gmail.com', 'password': ''}
        response = self.client.post(signup_url, payload)
        self.assertEqual(400, response.status_code)

    def test_no_user_profile_created(self):
        user = User.objects.create(email='test@test.com')
        UserProfile.objects.filter(user=user).delete()
        user.delete()
        assert not UserProfile.objects.filter(user=user).exists()

    def test_user_profile_created(self):
        user = User.objects.create(email='test@test.com')
        assert UserProfile.objects.filter(user=user).exists()

    def test_user_profile_not_updated(self):
        user = User.objects.create(email='test@test.com')
        UserProfile.objects.filter(user=user).delete()
        user.email = 'new@test.com'
        user.save()
        assert not UserProfile.objects.filter(user=user).exists()

    def test_user_profile_with_correct_user(self):
        user = User.objects.create(email='test@test.com')
        profile = UserProfile.objects.get(user=user)
        assert profile.user == user

    def test_user_profile_with_correct_names(self):
        user = User.objects.create(email='test@test.com')
        UserProfile.objects.filter(user=user).update(first_name='John', last_name='Doe')
        profile = UserProfile.objects.get(user=user)
        assert profile.first_name == 'John'
        assert profile.last_name == 'Doe'

    def test_user_profile_with_correct_dates(self):
        user = User.objects.create(email='test@test.com')
        profile = UserProfile.objects.get(user=user)
        assert profile.created_at.date() == dt.now().date()
        assert profile.updated_at.date() == dt.now().date()
