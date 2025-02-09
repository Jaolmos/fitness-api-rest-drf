import pytest
from django.contrib.auth.models import User
from apps.users.models import UserProfile
from apps.users.api.serializers import UserSerializer, UserProfileSerializer

@pytest.mark.django_db
class TestUserProfileSerializer:
    
    def setup_method(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass1234',
            email='test@test.com'
        )
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            weight=80.5,
            height=180,
            age=30,
            experience_level='BEG',
            fitness_goal='STRENGTH',
            available_days=3
        )

    def test_user_serializer(self):
        """Test que el UserSerializer funciona correctamente"""
        serializer = UserSerializer(self.user)
        assert serializer.data['username'] == 'testuser'
        assert serializer.data['email'] == 'test@test.com'
        assert 'password' not in serializer.data  # password no debe estar en la respuesta

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
        """Test de validación de datos"""
        invalid_data = {
            'weight': -80,  # peso negativo
            'height': 180,
            'age': 30,
            'experience_level': 'INVALID',  # nivel inválido
            'fitness_goal': 'STRENGTH',
            'available_days': 3
        }
        
        serializer = UserProfileSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'weight' in serializer.errors
        assert 'experience_level' in serializer.errors
        

# pytest apps/users/tests/test_serializers.py -v