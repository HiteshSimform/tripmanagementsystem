from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionManager, PermissionsMixin
from django.utils.timezone import now
from .manager import UserManager
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICE = [
        ('admin','Admin'),
        ('trip_admin','Trip Admin'),
        ('participant','Trip Participant'),
        ('viewer','Viewer'),
        ('guest','Guest'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICE,default="guest")
    # is_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email
    

class EmailVerification(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

