from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['email','username','password','confirm_password','role']

    def validate_role(self,value):
        allowed_roles= ['guest','participant','viewer']
        if value not in allowed_roles:
            raise serializers.ValidationError("You are not allowed to register with this roles")
        return value
    
    def validate(self,data):
        if data['password']!= data['confirm_password']:
            raise serializers.ValidationError("Password do not match")
        return data

    def create(self,validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
        