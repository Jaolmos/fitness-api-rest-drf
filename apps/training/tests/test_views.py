import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from apps.training.models import TrainingPlan

@pytest.mark.django_db
class TestTrainingPlanViews:
    def setup_method(self):
        self.client = APIClient()
        
        # Crear usuario para las pruebas
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        
        # URLs
        self.list_create_url = reverse('training-plan-list')
        self.token_url = reverse('token_obtain_pair')
        
        # Datos de ejemplo para plan
        self.plan_data = {
            'plan_type': 'STRENGTH',
            'difficulty': 'BEG',
            'exercises': {
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
            },
            'is_active': True
        }

        # Login y obtener token
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_training_plan(self):
        """Test crear un plan de entrenamiento"""
        response = self.client.post(
            self.list_create_url, 
            self.plan_data,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['plan_type'] == 'STRENGTH'
        assert response.data['user']['username'] == 'testuser'

    def test_list_training_plans(self):
        """Test listar planes de entrenamiento"""
        # Crear algunos planes
        TrainingPlan.objects.create(user=self.user, **self.plan_data)
        TrainingPlan.objects.create(user=self.user, **self.plan_data)
        
        response = self.client.get(self.list_create_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_get_training_plan_detail(self):
        """Test obtener detalle de un plan"""
        plan = TrainingPlan.objects.create(user=self.user, **self.plan_data)
        url = reverse('training-plan-detail', kwargs={'pk': plan.pk})
        
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == plan.id

    def test_update_training_plan(self):
        """Test actualizar un plan"""
        plan = TrainingPlan.objects.create(user=self.user, **self.plan_data)
        url = reverse('training-plan-detail', kwargs={'pk': plan.pk})
        
        updated_data = self.plan_data.copy()
        updated_data['difficulty'] = 'INT'
        
        response = self.client.put(
            url, 
            updated_data,
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['difficulty'] == 'INT'

    def test_delete_training_plan(self):
        """Test eliminar un plan"""
        plan = TrainingPlan.objects.create(user=self.user, **self.plan_data)
        url = reverse('training-plan-detail', kwargs={'pk': plan.pk})
        
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not TrainingPlan.objects.filter(id=plan.id).exists()
