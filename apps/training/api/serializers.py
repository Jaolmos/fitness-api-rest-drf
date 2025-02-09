from rest_framework import serializers
from apps.training.models import TrainingPlan
from apps.users.api.serializers import UserSerializer


class TrainingPlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TrainingPlan
        fields = (
            'id',
            'user',
            'plan_type',
            'difficulty',
            'exercises',
            'created_at',
            'is_active'
        )

    def validate_exercises(self, value):
        """Validación del formato JSON de exercises"""
        if not isinstance(value, dict) or 'dias' not in value:
            raise serializers.ValidationError(
                "El formato de exercises debe ser un diccionario con una clave 'dias'"
            )
        return value
