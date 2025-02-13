from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserProfile(models.Model):
    EXPERIENCE_LEVELS = [
        ('BEG', 'Principiante'),
        ('INT', 'Intermedio'),
        ('ADV', 'Avanzado'),
    ]

    GOALS = [
        ('HYPERTROPHY', 'Hipertrofia/Ganar Músculo'),
        ('STRENGTH', 'Fuerza Máxima'),
        ('ENDURANCE', 'Resistencia'),
        ('WEIGHT_LOSS', 'Pérdida de Peso'),
        ('MAINTENANCE', 'Mantenimiento'),
    ]

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        default='M',
        verbose_name='Género'
    )
    weight = models.FloatField()
    height = models.FloatField()
    age = models.IntegerField()
    experience_level = models.CharField(max_length=3, choices=EXPERIENCE_LEVELS)
    fitness_goal = models.CharField(max_length=20, choices=GOALS)
    available_days = models.IntegerField(default=3)
    health_conditions = models.TextField(blank=True)

    def clean(self):
        if self.weight <= 0:
            raise ValidationError('El peso debe ser mayor que 0')
        
        if self.experience_level not in dict(self.EXPERIENCE_LEVELS):
            raise ValidationError('Nivel de experiencia no válido')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Perfil de {self.user.username}'