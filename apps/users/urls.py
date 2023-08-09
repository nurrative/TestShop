from django.urls import path
from .views import CustomTokenRefreshView, CustomTokenObtainPairView, RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('login/jwt/refresh/', CustomTokenRefreshView.as_view(), name="jwt-refresh"),
]