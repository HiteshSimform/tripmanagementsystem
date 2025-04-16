from django.urls import path
from .views import RegisterAPIView, VerifyEmail
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("allusers/", RegisterAPIView.as_view(), name="allusers"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("email-verify/", VerifyEmail.as_view(), name="email-verify"),
    path("register/<int:pk>/", RegisterAPIView.as_view(), name="register-detail"),
    path("register/delete/<int:pk>/", RegisterAPIView.as_view(), name="delete-user"),
]
