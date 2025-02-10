from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.training.models import TrainingPlan
from apps.training.api.serializers import TrainingPlanSerializer

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