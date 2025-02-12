from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.users.models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            weight=1, 
            height=1,  
            age=18,    
            experience_level='BEG',
            fitness_goal='STRENGTH'
        )