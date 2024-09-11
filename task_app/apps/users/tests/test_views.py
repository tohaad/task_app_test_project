from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.tests.factories import TEST_USER_PASSWORD


class TestUserRegisterAPIView:
    action_url = reverse('api:users:register')

    def test_post_action_succeed(self, api_client):
        assert not User.objects.exists()
        assert not Token.objects.exists()

        payload = {
            'username': 'test_username',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@mail.com',
            'password': 'test123',
            'password2': 'test123',
        }
        response = api_client.post(self.action_url, data=payload)
        assert response.status_code == status.HTTP_201_CREATED

        assert 'token' in response.data
        assert response.data['token'] is not None
        assert 'password' not in response.data
        assert 'password2' not in response.data

        created_user = User.objects.first()
        assert created_user
        assert created_user.username == payload['username']
        assert created_user.first_name == payload['first_name']
        assert created_user.last_name == payload['last_name']
        assert created_user.email == payload['email']
        assert created_user.auth_token
        assert created_user.auth_token.key == response.data['token']

    def test_post_action_failed(self, api_client):
        assert not User.objects.exists()

        payload = {}
        response = api_client.post(self.action_url, data=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert not User.objects.exists()


class TestUserLoginAPIView:
    action_url = reverse('api:users:login')

    def test_post_action_succeed(self, api_client, user):
        assert not Token.objects.exists()

        payload = {
            'username': user.username,
            'password': TEST_USER_PASSWORD
        }
        response = api_client.post(self.action_url, data=payload)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

        user.refresh_from_db()
        assert user.auth_token
        assert user.auth_token.key == response.data['token']

    def test_post_action_failed(self, api_client, user):
        assert not Token.objects.exists()

        payload = {
            'username': user.username,
            'password': 'abracadabra'
        }
        response = api_client.post(self.action_url, data=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Unable to log in with provided credentials.' in response.data['non_field_errors']

        assert not Token.objects.exists()


class TestUserLogoutAPIView:
    action_url = reverse('api:users:logout')

    def test_post_action_succeed(self, api_client, user):
        token = Token.objects.create(user=user)
        api_client.force_authenticate(user)

        assert Token.objects.filter(user=user).exists()

        response = api_client.post(self.action_url)
        assert response.status_code == status.HTTP_200_OK

        assert not Token.objects.filter(user=user).exists()

    def test_post_action_failed(self, api_client):
        response = api_client.post(self.action_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'Authentication credentials were not provided.' in response.data['detail']


class TestUserAuthenticationCheckAPIView:
    action_url = reverse('api:users:auth-check')

    def test_get_action_succeed(self, api_client, user):
        Token.objects.create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {user.auth_token.key}')
        response = api_client.get(self.action_url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_action_failed(self, api_client):
        response = api_client.get(self.action_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
