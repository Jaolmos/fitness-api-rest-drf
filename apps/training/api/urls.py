from django.urls import path
from apps.training.api.views import TrainingPlanListCreateView, TrainingPlanDetailView, GenerateTrainingPlanView

urlpatterns = [
    path('', TrainingPlanListCreateView.as_view(), name='training-plan-list'),
    path('<int:pk>/', TrainingPlanDetailView.as_view(), name='training-plan-detail'),
    path('generate/', GenerateTrainingPlanView.as_view(), name='generate-training-plan'),
]