from django.urls import path, include
from . import views
# from rest_framework.authtoken.views import ObtainAuthToken

app_name = 'accounts-api-v1'



urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.CustomObtainAuthToken.as_view(), name='login'),
]