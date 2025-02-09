import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from apps.training.models import TrainingPlan


@pytest.mark.django_db
class TestTrainingPlan:

    def setup_method(self):
        # Crear usuario para las pruebas
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass1234'
        )
        # Datos de ejemplo para ejercicios
        self.example_exercises = {
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

    def test_create_plan(self):
        """Test de creación básica de un plan"""
        plan = TrainingPlan.objects.create(
            user=self.user,
            plan_type='STRENGTH',
            difficulty='BEG',
            exercises=self.example_exercises,
            is_active=True
        )

        assert plan.user == self.user
        assert plan.plan_type == 'STRENGTH'
        assert plan.difficulty == 'BEG'
        assert plan.exercises == self.example_exercises
        assert plan.is_active == True
        assert plan.created_at is not None

    def test_invalid_plan_type(self):
        """Test que el tipo de plan debe ser válido"""
        with pytest.raises(ValidationError):
            TrainingPlan.objects.create(
                user=self.user,
                plan_type='INVALID',  # Tipo inválido
                difficulty='BEG',
                exercises=self.example_exercises
            )

    def test_invalid_difficulty(self):
        """Test que la dificultad debe ser válida"""
        with pytest.raises(ValidationError):
            TrainingPlan.objects.create(
                user=self.user,
                plan_type='STRENGTH',
                difficulty='INVALID',  # Dificultad inválida
                exercises=self.example_exercises
            )

    def test_str_method(self):
        """Test del método __str__"""
        plan = TrainingPlan.objects.create(
            user=self.user,
            plan_type='STRENGTH',
            difficulty='BEG',
            exercises=self.example_exercises
        )
        expected_str = f'Plan de Fuerza/Gimnasio para {self.user.username}'
        assert str(plan) == expected_str

    def test_multiple_plans_per_user(self):
        """Test que un usuario puede tener múltiples planes"""
        plan1 = TrainingPlan.objects.create(
            user=self.user,
            plan_type='STRENGTH',
            difficulty='BEG',
            exercises=self.example_exercises
        )

        plan2 = TrainingPlan.objects.create(
            user=self.user,
            plan_type='CARDIO',
            difficulty='INT',
            exercises=self.example_exercises
        )

        user_plans = TrainingPlan.objects.filter(user=self.user)
        assert user_plans.count() == 2

    def test_ordering(self):
        """Test que los planes se ordenan por fecha de creación descendente"""
        plan1 = TrainingPlan.objects.create(
            user=self.user,
            plan_type='STRENGTH',
            difficulty='BEG',
            exercises=self.example_exercises
        )
        plan2 = TrainingPlan.objects.create(
            user=self.user,
            plan_type='CARDIO',
            difficulty='INT',
            exercises=self.example_exercises
        )
        
        plans = TrainingPlan.objects.all()
        # Verificamos que las fechas estén en orden descendente
        assert plans[0].created_at >= plans[1].created_at
        
        # pytest apps/training/tests/test_models.py -v