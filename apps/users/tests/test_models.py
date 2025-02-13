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
        # Obtenemos el perfil creado automáticamente por el signal
        profile = self.user.profile
        
        # Actualizamos los valores que queremos testear
        profile.weight = 80.5
        profile.height = 180
        profile.age = 30
        profile.experience_level = 'BEG'
        profile.fitness_goal = 'STRENGTH'
        profile.available_days = 3
        profile.save()
        
        assert profile.user == self.user
        assert profile.weight == 80.5
        assert profile.height == 180
        assert profile.age == 30
        assert profile.experience_level == 'BEG'
        assert profile.fitness_goal == 'STRENGTH'
        assert profile.available_days == 3

    def test_user_one_profile(self):
        """Test que verifica que un usuario no puede tener más de un perfil"""
        # Ya existe un perfil para self.user. Intentar crear uno nuevo debe fallar.
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
        profile = self.user.profile
        assert str(profile) == f'Perfil de {self.user.username}'

    def test_invalid_weight(self):
        """Test que el peso no puede ser negativo"""
        profile = self.user.profile
        profile.weight = -80.5
        with pytest.raises(ValidationError):
            profile.save()

    def test_invalid_experience_level(self):
        """Test que el nivel de experiencia debe ser uno de los permitidos"""
        profile = self.user.profile
        profile.experience_level = 'INVALID'
        with pytest.raises(ValidationError):
            profile.save()

    def test_default_available_days(self):
        """Test que available_days tiene valor por defecto 3"""
        profile = self.user.profile
        # Si no se modifica, debe mantener el default definido en el modelo
        assert profile.available_days == 3

    def test_update_profile(self):
        """Test de actualización de datos del perfil"""
        profile = self.user.profile
        profile.weight = 82.0
        profile.experience_level = 'INT'
        profile.save()
        
        updated_profile = UserProfile.objects.get(id=profile.id)
        assert updated_profile.weight == 82.0
        assert updated_profile.experience_level == 'INT'
    
    # Tests adicionales para el campo gender
    def test_default_gender(self):
        """Test que el género por defecto es 'M'"""
        profile = self.user.profile
        assert profile.gender == 'M'
    
    def test_change_gender(self):
        """Test que se puede cambiar el género a 'F'"""
        profile = self.user.profile
        profile.gender = 'F'
        profile.save()
        updated_profile = UserProfile.objects.get(user=self.user)
        assert updated_profile.gender == 'F'
    
    def test_invalid_gender(self):
        """Test que asignar un género inválido lanza ValidationError"""
        profile = self.user.profile
        profile.gender = 'X'  # Valor inválido no definido en GENDER_CHOICES
        with pytest.raises(ValidationError):
            profile.full_clean()
