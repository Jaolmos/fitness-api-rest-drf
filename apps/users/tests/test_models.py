import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from apps.users.models import UserProfile

@pytest.mark.django_db
class TestUserProfile:
    
    def setup_method(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass1234'
        )

    def test_create_profile(self):
        """Test de creación básica de un perfil"""
        profile = UserProfile.objects.create(
            user=self.user,
            weight=80.5,
            height=180,
            age=30,
            experience_level='BEG',
            fitness_goal='STRENGTH',
            available_days=3
        )
        
        assert profile.user == self.user
        assert profile.weight == 80.5
        assert profile.height == 180
        assert profile.age == 30
        assert profile.experience_level == 'BEG'
        assert profile.fitness_goal == 'STRENGTH'
        assert profile.available_days == 3

    def test_user_one_profile(self):
        """Test que verifica que un usuario no puede tener más de un perfil"""
        UserProfile.objects.create(
            user=self.user,
            weight=80.5,
            height=180,
            age=30,
            experience_level='BEG',
            fitness_goal='STRENGTH'
        )
        
        with pytest.raises(IntegrityError):
            UserProfile.objects.create(
                user=self.user,
                weight=75,
                height=175,
                age=25,
                experience_level='INT',
                fitness_goal='HYPERTROPHY'
            )

    def test_str_method(self):
        """Test del método __str__"""
        profile = UserProfile.objects.create(
            user=self.user,
            weight=80.5,
            height=180,
            age=30,
            experience_level='BEG',
            fitness_goal='STRENGTH'
        )
        
        assert str(profile) == f'Perfil de {self.user.username}'

    def test_invalid_weight(self):
        """Test que el peso no puede ser negativo"""
        with pytest.raises(ValidationError):
            UserProfile.objects.create(
                user=self.user,
                weight=-80.5,
                height=180,
                age=30,
                experience_level='BEG',
                fitness_goal='STRENGTH'
            )

    def test_invalid_experience_level(self):
        """Test que el nivel de experiencia debe ser uno de los permitidos"""
        with pytest.raises(ValidationError):
            UserProfile.objects.create(
                user=self.user,
                weight=80.5,
                height=180,
                age=30,
                experience_level='INVALID',
                fitness_goal='STRENGTH'
            )

    def test_default_available_days(self):
        """Test que available_days tiene valor por defecto 3"""
        profile = UserProfile.objects.create(
            user=self.user,
            weight=80.5,
            height=180,
            age=30,
            experience_level='BEG',
            fitness_goal='STRENGTH'
        )
        assert profile.available_days == 3

    def test_update_profile(self):
        """Test de actualización de datos del perfil"""
        profile = UserProfile.objects.create(
            user=self.user,
            weight=80.5,
            height=180,
            age=30,
            experience_level='BEG',
            fitness_goal='STRENGTH'
        )
        
        profile.weight = 82.0
        profile.experience_level = 'INT'
        profile.save()
        
        updated_profile = UserProfile.objects.get(id=profile.id)
        assert updated_profile.weight == 82.0
        assert updated_profile.experience_level == 'INT'
        
        # pytest apps/users/tests/test_models.py -v