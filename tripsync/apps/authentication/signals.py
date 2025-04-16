from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.users.models import User


@receiver(pre_save, sender=User)
def cache_user_activation_status(sender, instance, **kwargs):
    try:
        old_instance = User.objects.get(pk=instance.pk)
        instance._was_inactive = not old_instance.is_active and instance.is_active
    except User.DoesNotExist:
        instance._was_inactive = False


@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if not created and hasattr(instance, "_was_inactive") and instance._was_inactive:
        print(">>> Sending welcome email to:", instance.email)

        send_mail(
            subject="Welcome to TripSync!",
            message=f"Hi {instance.username}, thank you for verifying your email and joining TripSync!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )
