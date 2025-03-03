from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.training.services.openai_service import OpenAIService
from apps.training.models import TrainingPlan
from apps.training.api.serializers import TrainingPlanSerializer
import logging



class TrainingPlanListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear planes de entrenamiento"""
    serializer_class = TrainingPlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Filtrar planes por usuario actual"""
        return TrainingPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Asignar usuario actual al crear plan"""
        serializer.save(user=self.request.user)

class TrainingPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vista para ver, actualizar y eliminar un plan específico"""
    serializer_class = TrainingPlanSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Filtrar planes por usuario actual"""
        return TrainingPlan.objects.filter(user=self.request.user)
    
    
class GenerateTrainingPlanView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrainingPlanSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("DEBUG: Iniciando generación de plan de entrenamiento")
            
            # Obtener los datos del perfil del usuario
            profile = request.user.profile
            print(f"DEBUG: Perfil encontrado - Usuario: {request.user.username}")
            print(f"DEBUG: Datos del perfil - Nivel: {profile.experience_level}, "
                  f"Objetivo: {profile.fitness_goal}, "
                  f"Días disponibles: {profile.available_days}")
            
            # Inicializar el servicio de OpenAI
            openai_service = OpenAIService()
            
            try:
                # Generar el plan
                plan_data = openai_service.generate_training_plan(
                    experience_level=profile.experience_level,
                    fitness_goal=profile.fitness_goal,
                    available_days=profile.available_days,
                    health_conditions=profile.health_conditions
                )
                print("DEBUG: Plan generado correctamente")
                
            except Exception as e:
                print(f"DEBUG: Error al generar el plan - {str(e)}")
                raise
                
            # Crear el plan en la base de datos
            plan = TrainingPlan.objects.create(
                user=request.user,
                plan_type='STRENGTH',
                difficulty=profile.experience_level,
                exercises=plan_data,
                is_active=True
            )
            
            serializer = self.get_serializer(plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"DEBUG: Error general en create - {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )