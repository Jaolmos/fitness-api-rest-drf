from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'weight', 'height', 'experience_level', 'fitness_goal', 'available_days')
    list_filter = ('gender', 'experience_level', 'fitness_goal')
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)
