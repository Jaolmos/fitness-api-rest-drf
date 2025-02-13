import pytest
from django.contrib.auth.models import User
from apps.users.models import UserProfile
from apps.users.api.serializers import UserSerializer, UserProfileSerializer
from rest_framework.test import APIRequestFactory

@pytest.mark.django_db
class TestUserProfileSerializer:
    
    def setup_method(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass1234',
            email='test@test.com'
        )
        
        # Usar el perfil creado automáticamente por el signal, en lugar de crearlo manualmente.
        self.user_profile = self.user.profile
        
        # Actualizar los campos del perfil con los datos de prueba
        self.user_profile.weight = 80.5
        self.user_profile.height = 180
        self.user_profile.age = 30
        self.user_profile.experience_level = 'BEG'
        self.user_profile.fitness_goal = 'STRENGTH'
        self.user_profile.available_days = 3
        self.user_profile.save()
        
        # Crear un request simulado para pasar al contexto del serializer
        factory = APIRequestFactory()
        self.request = factory.get("/")
        self.request.user = self.user

    def test_user_serializer(self):
        """Test que el UserSerializer funciona correctamente"""
        serializer = UserSerializer(self.user)
        assert serializer.data['username'] == 'testuser'
        assert serializer.data['email'] == 'test@test.com'
        # El campo password no debe estar en la respuesta
        assert 'password' not in serializer.data

    def test_profile_serializer(self):
        """Test que el UserProfileSerializer funciona correctamente"""
        serializer = UserProfileSerializer(self.user_profile)
        data = serializer.data
        
        assert data['weight'] == 80.5
        assert data['height'] == 180
        assert data['age'] == 30
        assert data['experience_level'] == 'BEG'
        assert data['fitness_goal'] == 'STRENGTH'
        assert data['available_days'] == 3
        
        # Verificar datos del usuario anidado
        assert data['user']['username'] == 'testuser'
        assert data['user']['email'] == 'test@test.com'

    def test_profile_serializer_validation(self):
        """Test de validación de datos del serializer para datos inválidos"""
        invalid_data = {
            'weight': -80,  # peso negativo
            'height': 180,
            'age': 30,
            'experience_level': 'INVALID',  # nivel inválido
            'fitness_goal': 'STRENGTH',
            'available_days': 3
        }
        
        serializer = UserProfileSerializer(data=invalid_data, context={'request': self.request})
        assert not serializer.is_valid()
        # Se esperan errores en 'weight' y 'experience_level'
        assert 'weight' in serializer.errors
        assert 'experience_level' in serializer.errors
