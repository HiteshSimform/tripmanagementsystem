# from django.urls import path
# from apps.authentication.views import LoginAPIView, LogoutAPIView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )
# urlpatterns = [
#     # path("login/", LoginAPIView.as_view(), name="login"),
#     path('login/', TokenObtainPairView.as_view(), name='jwt-login'),
#     path("logout/", LogoutAPIView.as_view(), name="logout"),
# ]


from django.urls import path
from apps.authentication.views import LoginAPIView, LogoutAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain"),  
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
