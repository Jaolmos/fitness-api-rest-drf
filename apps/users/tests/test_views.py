import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.users.models import UserProfile

@pytest.mark.django_db
class TestUserViews:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.token_url = reverse('token_obtain_pair')
        self.profile_url = reverse('user-profile')
        
        # Datos para pruebas
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@test.com'
        }
        
        self.profile_data = {
            'weight': 80.5,
            'height': 180,
            'age': 30,
            'experience_level': 'BEG',
            'fitness_goal': 'STRENGTH',
            'available_days': 3
        }

    def test_user_registration(self, client):
        """Test del registro de usuario"""
        response = client.post(self.register_url, self.user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert User.objects.get().username == 'testuser'

    def test_user_login(self, client):
        """Test del login de usuario"""
        # Crear usuario primero
        User.objects.create_user(**self.user_data)
        
        # Intentar login
        response = client.post(self.token_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_get_profile_unauthorized(self, client):
        """Test que usuario no autenticado no puede ver perfil"""
        response = client.get(self.profile_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_profile(self):
        """Test que usuario autenticado puede ver su perfil"""
        # Crear usuario y perfil
        user = User.objects.create_user(**self.user_data)
        profile = UserProfile.objects.create(user=user, **self.profile_data)
        
        # Obtener token
        response = self.client.post(self.token_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        token = response.data['access']
        
        # Hacer petición con token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.profile_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['weight'] == self.profile_data['weight']
        
        
        # pytest apps/users/tests/test_views.py -v