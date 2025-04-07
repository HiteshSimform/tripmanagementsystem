from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.decorators import api_view
from apps.users.models import User
from django.conf import settings

import smtplib
smtplib.SMTP.debuglevel = 1

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # user = serializer.save()
            serializer.save()
            # send_mail(
            #     subject="Welcome to Our Platform!",
            #     message=f"Hi {user.username}, thank you for registering!",
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[user.email],
            #     fail_silently=False,
            # )
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        users = User.objects.all()
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

