from django.urls import path
from apps.training.api.views import TrainingPlanListCreateView, TrainingPlanDetailView

urlpatterns = [
    path('', TrainingPlanListCreateView.as_view(), name='training-plan-list'),
    path('<int:pk>/', TrainingPlanDetailView.as_view(), name='training-plan-detail'),
]