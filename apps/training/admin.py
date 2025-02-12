from django.contrib import admin
from apps.training.models import TrainingPlan

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_type', 'difficulty', 'get_exercises_summary', 'is_active', 'created_at')
    list_filter = ('plan_type', 'difficulty', 'is_active')
    search_fields = ('user__username',)

    def get_exercises_summary(self, obj):
        """Muestra un resumen de los ejercicios del plan"""
        if obj.exercises and 'dias' in obj.exercises:
            dias = len(obj.exercises['dias'])
            total_ejercicios = sum(len(dia['ejercicios']) for dia in obj.exercises['dias'])
            return f"{dias} días, {total_ejercicios} ejercicios"
        return "Sin ejercicios"
    
    get_exercises_summary.short_description = "Ejercicios"