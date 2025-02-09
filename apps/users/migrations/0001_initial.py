# Generated by Django 5.1.6 on 2025-02-09 08:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('age', models.IntegerField()),
                ('experience_level', models.CharField(choices=[('BEG', 'Principiante'), ('INT', 'Intermedio'), ('ADV', 'Avanzado')], max_length=3)),
                ('fitness_goal', models.CharField(choices=[('HYPERTROPHY', 'Hipertrofia/Ganar Músculo'), ('STRENGTH', 'Fuerza Máxima'), ('ENDURANCE', 'Resistencia'), ('WEIGHT_LOSS', 'Pérdida de Peso'), ('MAINTENANCE', 'Mantenimiento')], max_length=20)),
                ('available_days', models.IntegerField(default=3)),
                ('health_conditions', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
