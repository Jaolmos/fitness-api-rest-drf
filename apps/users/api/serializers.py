from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'weight',
            'height',
            'age',
            'experience_level',
            'fitness_goal',
            'available_days',
            'health_conditions'
        )

    def validate_weight(self, value):
        """Validación personalizada para el peso"""
        if value <= 0:
            raise serializers.ValidationError("El peso debe ser mayor que 0")
        return value
