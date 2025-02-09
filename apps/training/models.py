# apps/training/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class TrainingPlan(models.Model):
    TRAINING_TYPES = [
        ('STRENGTH', 'Fuerza/Gimnasio'),
        ('CARDIO', 'Cardiovascular'),
        ('HIIT', 'HIIT'),
        ('MIXED', 'Mixto'),
    ]

    DIFFICULTY_LEVELS = [
        ('BEG', 'Principiante'),
        ('INT', 'Intermedio'),
        ('ADV', 'Avanzado'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='training_plans',
        verbose_name='Usuario'
    )

    plan_type = models.CharField(
        max_length=50, 
        choices=TRAINING_TYPES,
        verbose_name='Tipo de entrenamiento'
    )

    difficulty = models.CharField(
        max_length=3, 
        choices=DIFFICULTY_LEVELS,
        verbose_name='Nivel de dificultad'
    )

    exercises = models.JSONField(
        verbose_name='Ejercicios',
        help_text='Estructura del plan de ejercicios'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Plan activo'
    )

    class Meta:
        verbose_name = 'Plan de entrenamiento'
        verbose_name_plural = 'Planes de entrenamiento'
        ordering = ['-created_at']

    def __str__(self):
        return f'Plan de {self.get_plan_type_display()} para {self.user.username}'

    def clean(self):
        if self.plan_type not in dict(self.TRAINING_TYPES):
            raise ValidationError('Tipo de entrenamiento no válido')
        if self.difficulty not in dict(self.DIFFICULTY_LEVELS):
            raise ValidationError('Nivel de dificultad no válido')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)