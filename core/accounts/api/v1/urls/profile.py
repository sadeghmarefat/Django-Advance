from django.urls import path
from accounts.api.v1 import views

app_name = "accounts-api-v1"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
