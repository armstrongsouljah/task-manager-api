from django.test import TestCase, Client

# Create your tests here.
class RegistrationTest(TestCase):
    """ Test user registration implementation """
    def setUp(self):
        self.client = Client()

    def test_sucessful_user_signup(self):
        signup_url = '/auth/users/register/'
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'Password2'
        }
        response = self.client.post(signup_url, payload)
        self.assertEqual(201, response.status_code)

    def test_signup_with_invalid_email(self):
        signup_url = '/auth/users/register/'
        payload = {
            'email': 'testusergmail.com',
            'password': 'Password2'
        }
        response = self.client.post(signup_url, payload)
        self.assertEqual(400, response.status_code)

    def test_signup_without_password_fails(self):
        signup_url = '/auth/users/register/'
        payload = {
            'email': 'testuser@gmail.com',
            'password': ''
        }
        response = self.client.post(signup_url, payload)
        self.assertEqual(400, response.status_code)