from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.decorators import api_view
from apps.users.models import User, EmailVerification
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken

import smtplib

smtplib.SMTP.debuglevel = 1


class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer.send_activation_email(user)
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = User.objects.all()
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserRegistrationSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserRegistrationSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(
                {"message": "User deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class VerifyEmail(APIView):
    permission_classes = []

    def get(self, request):
        token = request.GET.get("token")
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)

            if not user.is_active:
                user.is_active = True
                user.save()

            ev = EmailVerification.objects.get(user=user)
            ev.is_verified = True
            ev.save()

            return Response(
                {"msg": "Email verified successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            print(str(e))
            return Response(
                {"msg": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST
            )


# reset password
# confirmpassword
# change password
#
