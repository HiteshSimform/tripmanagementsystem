from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.users.models import User
@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if created:
        user_email = instance.email
        send_mail(
            subject="Welcome to TripSync!",
            message=f"Hi {instance.username}, thank you for registering!",
            recipient_list=[user_email],
            fail_silently=False,
        )
