from django.urls import path, include
from .views import RegisterAPIView, VerifyEmail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('allusers/',RegisterAPIView.as_view(),name='allusers'),
    path('',include('apps.authentication.urls')),
    # path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('register/<int:pk>/', RegisterAPIView.as_view(), name='register-detail'),
]
