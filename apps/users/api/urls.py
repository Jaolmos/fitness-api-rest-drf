from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.users.api.views import UserRegistrationView, UserProfileView

urlpatterns = [
    # Auth URLs
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # User URLs
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
]