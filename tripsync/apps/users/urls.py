from django.urls import path, include
from .views import RegisterAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('allusers/',RegisterAPIView.as_view(),name='allusers'),
    path('',include('apps.authentication.urls'))
]
