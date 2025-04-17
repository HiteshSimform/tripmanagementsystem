from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
import os
from dotenv import load_dotenv
from .models import EmailVerification

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        token = RefreshToken.for_user(user).access_token
        EmailVerification.objects.create(user=user, token=str(token))
        self.send_activation_email(user)
        return user

    def send_activation_email(self, user):
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(self.context["request"]).domain
        relative_link = reverse("email-verify")
        absurl = f"http://{current_site}{relative_link}?token={str(token)}"
        email_body = (
            f"Hi {user.username}, Use the link to verify your account:\n{absurl}"
        )
        send_mail(
            subject="Verify your email",
            message=email_body,
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[user.email],
        )


# --- User Serializer (Light version for join request) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
