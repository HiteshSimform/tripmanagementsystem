from django.db import models
from apps.users.models import User


# Create your models here.
class BlacklistedToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jti = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.email} blacklisted at {self.blacklisted_at}"
