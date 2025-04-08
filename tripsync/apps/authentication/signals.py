from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.users.models import User
from apps.trips.models import Trip

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


@receiver(post_save, sender = User)
def update_role_on_registration(sender, instance, created, **kwargs):
    if created:
        instance.role = "Viewer"
        instance.save()

# 

@receiver(post_save, sender= Trip)
def update_role_on_trip_creation(sender, instance, created, **kwargs):
    if created and instance.creator.role in ["Viewer","participant"] :
        instance.creator.role = "trip_admin"
        instance.creator.save()

@receiver(post_save, sender= Trip)
def update_role_on_participation(sender,instance,**kwargs):
    for participant in instance.participants.all():
        if participant.role != "trip_admin":
            participant.role = "participant"
            participant.save()