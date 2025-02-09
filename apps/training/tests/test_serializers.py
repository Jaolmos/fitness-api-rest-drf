
import pytest
from django.contrib.auth.models import User
from apps.training.models import TrainingPlan
from apps.training.api.serializers import TrainingPlanSerializer

@pytest.mark.django_db
class TestTrainingPlanSerializer:
    
    def setup_method(self):
        # Crear usuario para las pruebas
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass1234',
            email='test@test.com'
        )
        
        # Datos de ejemplo para los ejercicios
        self.valid_exercises = {
            "dias": [
                {
                    "dia": "Lunes",
                    "ejercicios": [
                        {
                            "nombre": "Press de banca",
                            "series": 3,
                            "repeticiones": "12-15",
                            "descanso": "90 segundos"
                        }
                    ]
                }
            ]
        }
        
        # Crear plan de entrenamiento
        self.training_plan = TrainingPlan.objects.create(
            user=self.user,
            plan_type='STRENGTH',
            difficulty='BEG',
            exercises=self.valid_exercises,
            is_active=True
        )

    def test_training_plan_serializer(self):
        """Test que el TrainingPlanSerializer funciona correctamente"""
        serializer = TrainingPlanSerializer(self.training_plan)
        data = serializer.data
        
        assert data['plan_type'] == 'STRENGTH'
        assert data['difficulty'] == 'BEG'
        assert data['exercises'] == self.valid_exercises
        assert data['is_active'] == True
        assert data['user']['username'] == 'testuser'

    def test_invalid_exercises_format(self):
        """Test que valida el formato correcto de exercises"""
        invalid_data = {
            'user': self.user.id,
            'plan_type': 'STRENGTH',
            'difficulty': 'BEG',
            'exercises': {'invalid': 'format'},  # Formato inválido
            'is_active': True
        }
        
        serializer = TrainingPlanSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'exercises' in serializer.errors

    def test_invalid_plan_type(self):
        """Test que valida el tipo de plan"""
        invalid_data = {
            'user': self.user.id,
            'plan_type': 'INVALID',  # Tipo inválido
            'difficulty': 'BEG',
            'exercises': self.valid_exercises,
            'is_active': True
        }
        
        serializer = TrainingPlanSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'plan_type' in serializer.errors
        
        
# pytest apps/training/tests/test_serializers.py -v
