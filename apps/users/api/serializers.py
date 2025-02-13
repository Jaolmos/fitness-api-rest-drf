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

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'gender',
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

    def create(self, validated_data):
        """
        Si el perfil ya existe para el usuario, se actualiza; 
        de lo contrario se crea.
        Se espera que el usuario se pase en el contexto (self.context['request'].user)
        """
        request = self.context.get('request')
        if not request:
            raise serializers.ValidationError("El request debe estar en el contexto")
        user = request.user

        # Intenta obtener el perfil existente; si no existe, se crea.
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Actualiza los campos con los datos validados
        for attr, value in validated_data.items():
            setattr(profile, attr, value)
        profile.save()
        return profile
