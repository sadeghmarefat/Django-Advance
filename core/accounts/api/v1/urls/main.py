from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'accounts-api-v1'

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomLogoutTokenView.as_view(), name='token-logout'),
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='token-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
